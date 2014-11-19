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
from django.utils import simplejson

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
	entrada = Entrada(titulo=titulo,link=link,fecha=fecha,descripcion=descripcion)
	return entrada


#Devuelve una entrada
def ParsearEntrada(rss,i):
	entrada = ParsearEtiquetasRss(rss,i)
	return entrada


#Parsea el RSS
def ParsearRss(usuario):
	rss = ObtenerRss(usuario.rss)
	i = 0
	while i<len(rss.entries):
		entrada = ParsearEntrada(rss,i)
		entrada.usuario = usuario
		entrada.up = 0
		entrada.down = 0
		entrada.save()
		i = i + 1
	
	
#Main
def index(request):
	info = "Tus datos son erróneos. Introdúcelos otra vez."
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(Usuario.objects.all(), ensure_ascii=False)
	lista_usuarios = Usuario.objects.order_by('nombre_apellidos')

	json_entradas = json_serializer.serialize(Entrada.objects.all(), ensure_ascii=False)
	#lista_usuarios = ActualizarUsuarios()
	lista_entradas = Entrada.objects.order_by('-fecha')
	lista_entradas_valoradas = Entrada.objects.order_by('-up')[:4]
	
	paginator = Paginator(lista_entradas, 5) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	# If page is not an integer, deliver first page.
		entradas = paginator.page(1)
	except EmptyPage:	# If page is out of range (e.g. 9999), deliver last page of results.
		entradas = paginator.page(paginator.num_pages)
	
	return render(request,'planetablogs/index.html',{"entradas": entradas,'lista_entradas':lista_entradas,'lista_usuarios':lista_usuarios, 'lista_entradas_valoradas':lista_entradas_valoradas, 'json_usuarios':json_usuarios, 'json_entradas':json_entradas})


#Comprueba si ha sido exitoso el formulario (Sólo por nick. Implementar para contraseña)
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
				form.puntuaciontotal = 0
				form.nivel = 0
				form.entradas = 0
				form.url_blog = ''
				form.conectado = False
				form.save()
				usuarios = Usuario.objects.all()
				for usu in usuarios:
					if (usu.nick == form.nick):
						ParsearRss(usu)
						break;
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


def up(request):
	lista_entradas = Entrada.objects.order_by('-fecha')
	if request.method=='GET':
		entrada = Entrada.objects.filter(id=request.GET['id'])
		entrada.up = 1
		entrada.save()
		ctx = serializers.serialize('json', entrada)
		print ctx
	return HttpResponse(ctx, mimetype='application/json')
	
	
def down(request):
	lista_entradas = Entrada.objects.order_by('-fecha')
	if request.method=='GET':
		entrada = Entrada.objects.filter(id=request.GET['id'])
		ctx = serializers.serialize('json', entrada)
	return HttpResponse(ctx, mimetype='application/json')


#Pestaña de búsqueda
def buscar(request):
	return render(request, 'planetablogs/buscar.html')

#Buscar por nick de usuario
def buscarNickUsuario(request):
	if request.method=='GET':
		usu = Usuario.objects.filter(nick=request.GET['texto'])
		lista_entradas = Entrada.objects.filter(usuario=usu)
		json_serializer = serializers.get_serializer("json")()
		json_usuario = json_serializer.serialize(usu, ensure_ascii=False)
		json_entradas = json_serializer.serialize(lista_entradas, ensure_ascii=False)
	return render(request, 'planetablogs/buscar.html', {'lista_entradas':lista_entradas})
	'''return render(request, 'planetablogs/buscar.html', {'json_usuario':json_usuario,'json_entradas':json_entradas})'''
'''
#Buscar por nick de usuario
def buscarNickUsuario(request):
	if request.method=='GET':
		usu = Usuario.objects.filter(nick=request.GET['texto'])
		lista_entradas = Entrada.objects.filter(usuario=usu)
		json_serializer = serializers.get_serializer("json")()
		json_usuario = json_serializer.serialize(usu, ensure_ascii=False)
		json_entradas = json_serializer.serialize(lista_entradas, ensure_ascii=False)
		s1 = {'json_usuario':json_usuario, 'json_entradas':json_entradas}
		json = simplejson.dumps(s1, cls=simplejson.encoder.JSONEncoderForHTML)
	return HttpResponse(s1, mimetype='application/json')
'''


if __name__ == '__main__':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFG.settings")



	
'''
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
'''

'''
#Si alguien se identifica
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
'''