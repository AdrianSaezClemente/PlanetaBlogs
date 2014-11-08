#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from planetablogs.models import Entrada, Usuario
from planetablogs.formularios import FormularioRegistro, FormularioIdentidad
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import feedparser
from time import mktime
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


#Obtiene el RSS con feedparser
def ObtenerRss(url):
	rss = feedparser.parse(url)
	return rss
	

#Parsear las etiquetas del RSS y devuelve una entrada
def ParsearEtiquetasRss(rss,i):
	titulo = rss.entries[i].title
	link = rss.entries[i].link
	pubDate = rss.entries[i].published_parsed 
	fecha = datetime.fromtimestamp(mktime(pubDate))	#Convertir fecha a DateTime
	descripcion = rss.entries[i].description
	print descripcion+'\n\n'
	entrada = Entrada(titulo=titulo,link=link,fecha=fecha,descripcion=descripcion)
	return entrada


#Devuelve una entrada
def ParsearEntrada(rss,i):
	entrada = ParsearEtiquetasRss(rss,i)
	return entrada


#Parsea el RSS
def ParsearRss(usuario,lon):
	rss = ObtenerRss(usuario.rss)
	lista = []
	i = 0
	while i<lon:
		entrada = ParsearEntrada(rss,i)
		entrada.usuario = usuario
		entrada.save()
		i = i + 1


#Guarda la entrada en la bbdd
def GuardarEntradas(usuario,lon):
	ParsearRss(usuario,lon)


#Guarda entradas que son nuevas
def GuardarEntradasNuevas(usuario,nuevas):
	ParsearRss(usuario,nuevas)
	usuario.entradas = usuario.entradas + nuevas


#Comprueba si ha habido actualizacion de entradas en los RSS's
def ComprobarEntradas(usuario,lon,actualizacion):
	ent = usuario.entradas
	print "Entradas de "+usuario.nick+" en el rss: "+str(lon)
	print "Entradas del "+usuario.nick+" en la bbdd: "+str(ent)
	if ent<lon:
		nuevas = lon - ent
		print "Entradas nuevas de "+usuario.nick+" : "+str(nuevas)
		GuardarEntradasNuevas(usuario,nuevas)
		actualizacion = actualizacion + 1
	return actualizacion
		

#Actualiza usuarios
def ActualizarUsuarios():
	lista_usuarios = Usuario.objects.all()
	actualizacion = 0
	for usuario in lista_usuarios:
		rss = ObtenerRss(usuario.rss)
		lon = len(rss.entries)
		while i<lon:
			fecha = rss.entries[i].published_parsed
			fechaEntrada = datetime.fromtimestamp(mktime(fecha))
			print fechaEntrada
			if (fechaEntrada>now):
				titulo = rss.entries[i].title
				link = rss.entries[i].link
				descripcion = rss.entries[i].description
				entrada = Entrada(titulo=titulo,link=link,fecha=fechaEntrada,descripcion=descripcion)
			else:
				print "Es menor"+ fechaEntrada
				
	now = datetime.datetime.now()
	print now
	return render(request,'planetablogs/index.html',{"entradas": entradas,'lista_entradas':lista_entradas,'lista_usuarios':lista_usuarios,'json_usuarios':json_usuarios})


#Autenticar usuario con nick y clave (NO TERMINADO)
def autenticar(nick,clave):
	lista_usuarios = Usuario.objects.all()
	for x in lista_usuarios:
		if (x.nick == nick) & (x.password == clave):
			salir = True
			x.conectado = True
			x.save()
			break
		else:
			salir = False
	return salir	


#Main
def index(request):
	info = "Tus datos son erróneos. Introdúcelos otra vez."
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(Usuario.objects.all(), ensure_ascii=False)
	lista_usuarios = Usuario.objects.order_by('nombre_apellidos')
	json_entradas = json_serializer.serialize(Entrada.objects.all(), ensure_ascii=False)
	#lista_usuarios = ActualizarUsuarios()
	lista_entradas = Entrada.objects.order_by('-fecha')
	json_puntuaciones = json_serializer.serialize(Puntuacion.objects.all(), ensure_ascii=False)
	lista_puntuaciones = Puntuacion.objects()
	
	paginator = Paginator(lista_entradas, 5) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	# If page is not an integer, deliver first page.
		entradas = paginator.page(1)
	except EmptyPage:	# If page is out of range (e.g. 9999), deliver last page of results.
		entradas = paginator.page(paginator.num_pages)
	
	if request.method=='POST':
		formulario = FormularioIdentidad(request.POST)
		if formulario.is_valid:
			nick = request.POST['nick']
			clave = request.POST['password']
			print "nick: "+str(nick)+" pass: "+str(clave)
			acceso = autenticar(nick,clave)
			print acceso
	else:
		formulario = FormularioIdentidad()
	return render(request,'planetablogs/index.html',{"entradas": entradas,'lista_entradas':lista_entradas,'lista_usuarios':lista_usuarios,'lista_puntuaciones':lista_puntuaciones, 'json_usuarios':json_usuarios, 'json_entradas':json_entradas, 'json_puntuaciones':json_puntuaciones})


#Mostrar tabla de usuarios registrados
def mostrarTabla(request):
	lista_entradas = Entrada.objects.all()
	return render_to_response('planetablogs/tabla.html',{'personas': personas })


#Comprueba si ha sido exitoso el formulario
def ComprobarRegistro(form):
	lista_usuarios = Usuario.objects.all()
	exitoso = True
	for usu in lista_usuarios:
		if (usu.nick == form.nick):
			exitoso = False
	return exitoso


#Introducir datos de registro
def nuevo_usuario(request):
	info = "False"
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(Usuario.objects.all(), ensure_ascii=False)
	if request.method=='POST':
		formulario = FormularioRegistro(request.POST)
		if formulario.is_valid():
			form = formulario.save(commit = False)
			exitoso = ComprobarRegistro(form)
			if(exitoso):
				form.entradas = 0
				form.url_blog = ''
				form.conectado = False
				form.save()
				return render(request, 'planetablogs/info.html', {'form': form})
			else:
				return render(request, 'planetablogs/nuevousuario.html', {'lista_usuarios':lista_usuarios,'info': info})
		else:
			return render(request, 'planetablogs/nuevousuario.html', {'lista_usuarios':lista_usuarios,'info': info})
	else:
		formulario = FormularioRegistro()
	return render(request, 'planetablogs/nuevousuario.html', {'formulario': formulario,'lista_usuarios':lista_usuarios})


#Pestaña de puntuaciones de usuarios
def puntuaciones(request):
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(Usuario.objects.all(), ensure_ascii=False)
	return render(request, 'planetablogs/puntuaciones.html', {'lista_usuarios':lista_usuarios})

#Pestaña de información de puntuaciones de usuarios
def infopuntuaciones(request):
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(Usuario.objects.all(), ensure_ascii=False)
	return render(request, 'planetablogs/infopuntuaciones.html', {'lista_usuarios':lista_usuarios})

#Pestaña de búsqueda
def buscar(request):
	return render(request, 'planetablogs/buscar.html')


if __name__ == '__main__':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFG.settings")
