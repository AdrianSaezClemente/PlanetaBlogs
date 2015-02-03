#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from planetablogs.models import Entrada, Alumno, Profesor, Asignatura, Rss
from planetablogs.formularios import FormularioRegistro, FormularioIdentidad, FormularioHilo, FormularioAgregarRSS
from django.contrib.auth.forms import UserCreationForm
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
from django.contrib import auth

'''
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
		entrada.save()
		i = i + 1
'''


#Introducir datos de registro de alumno
def nuevo_alumno(request):
	info = False
	if request.method == 'POST':
		form = FormularioRegistro(request.POST)
		if form.is_valid():
			info = True
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]

			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			
			alum = Alumno(alumno=user)
			alum.save()
			
			return HttpResponseRedirect(reverse('login'))  # Redirect after POST
		else:
			return render(request, 'planetablogs/nuevoalumno.html', {'info': info})
	else:
		form = FormularioRegistro()
	print info
	return render(request, 'planetablogs/nuevoalumno.html', {'info': info})



#Introducir datos de registro de profesor
def nuevo_profesor(request):
	info = False
	if request.method == 'POST':
		form = FormularioRegistro(request.POST)
		print info
		if form.is_valid():
			info = True
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]

			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			
			profe = Profesor(profesor=user)
			profe.save()
			
			return HttpResponseRedirect(reverse('login'))  # Redirect after POST
		else:
			return render(request, 'planetablogs/nuevoprofesor.html', {'info': info})
	else:
		form = FormularioRegistro()
	return render(request, 'planetablogs/nuevoprofesor.html', {'info': info})



#Comprobar si un usuario es alumno o profesor
def ComprobarUsuario(idusuario):
	alumnos = Alumno.objects.all()
	NoEncontrado = True
	for i in alumnos:
		if (i.alumno_id == idusuario):
			NoEncontrado = False
			usuario = "Alumno"
			break;
	if (NoEncontrado):
		usuario = "Profesor"
	return usuario



#Página de inicio. Registro e identificación.
def inicio(request):
	error = None
	if request.method == 'POST':
		username = request.POST.get('nick', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			error = False
			auth.login(request, user)
			usuario = ComprobarUsuario(user.id)
			if (usuario == "Alumno"):
				return HttpResponseRedirect(reverse('presentacionalumno'))
			else:
				return HttpResponseRedirect(reverse('presentacionprofesor'))
		else:
			error = True
			return render(request, 'planetablogs/inicio.html', {'login': error})
	return render(request, 'planetablogs/inicio.html', {'login': error})



#Eliminar asignatura de los hilos de un alumno
def eliminarasignaturaalumno(request):
	if request.method=='GET':
		hilo = Rss.objects.get(asignatura=request.GET['id'],alumno=request.user.id)
		print hilo
		hilo.delete()
		lista_asignaturas = Asignatura.objects.filter(alumnos=request.user.id)
		lista_no_asignaturas = Asignatura.objects.all().exclude(alumnos=request.user.id)
	return render(request,'planetablogs/presentacionalum.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})



#Se usa el formulario FormularioAgregarRSS para establecer una relación entre asignatura, alumno y RSS
@login_required()
def presentacionalumno(request):
	info = None
	idasignatura = 0
	asignaturas = Asignatura.objects.all()
	lista_asignaturas = Asignatura.objects.filter(alumnos=request.user.id)
	lista_no_asignaturas = Asignatura.objects.all().exclude(alumnos=request.user.id)
	print "soy un alumno"
	if request.method == 'POST':
		formRSS = FormularioAgregarRSS(request.POST)
		idasignatura = request.POST.get('asignatura', '')
		if formRSS.is_valid():
			info = False
			hilo = formRSS.save(commit=False)
			hilo.alumno_id = request.user.id
			hilo.save()
		else:
			info = True
	return render(request,'planetablogs/presentacionalum.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas, 'info': info, 'idasignatura':idasignatura})


		
#Agregar asignatura a los hilos de un profesor
def agregarasignaturaprofesor(request):
	if request.method=='GET':
		hilo = Asignatura.objects.get(id=request.GET['id'])
		hilo.profesores.add(request.user.id)
		lista_asignaturas = Asignatura.objects.filter(profesores=request.user.id)
		lista_no_asignaturas = Asignatura.objects.all().exclude(profesores=request.user.id)
	return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})



#Eliminar asignatura de los hilos de un profesor
def eliminarasignaturaprofesor(request):
	if request.method=='GET':
		hilo = Asignatura.objects.get(id=request.GET['id'])
		hilo.profesores.remove(request.user.id)
		lista_asignaturas = Asignatura.objects.filter(profesores=request.user.id)
		lista_no_asignaturas = Asignatura.objects.all().exclude(profesores=request.user.id)
	return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})



@login_required()
def presentacionprofesor(request):
	asignaturas = Asignatura.objects.all()
	lista_asignaturas = Asignatura.objects.filter(profesores=request.user.id)
	lista_no_asignaturas = Asignatura.objects.all().exclude(profesores=request.user.id)
	print "soy un profesor"
	if request.method == 'POST':
		formHilo = FormularioHilo(request.POST)
		if formHilo.is_valid():
			hilo = formHilo.save(commit=False)
			hilo.save()
			return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})
		else:
			print "NO VALIDO formHilo"
	return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})

	

@login_required()
def mostrarhilo(request,asignatura_id):
	'''
	info = "Tus datos son erróneos. Introdúcelos otra vez."
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(Alumno.objects.all(), ensure_ascii=False)
	lista_usuarios = Alumno.objects.order_by('nombre_apellidos')

	json_entradas = json_serializer.serialize(Entrada.objects.all(), ensure_ascii=False)
	lista_entradas_valoradas = Entrada.objects.order_by('-up')[:4]
	'''
	lista_entradas = Entrada.objects.order_by('-fecha')
	
	paginator = Paginator(lista_entradas, 5) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	# If page is not an integer, deliver first page.
		entradas = paginator.page(1)
	except EmptyPage:	# If page is out of range (e.g. 9999), deliver last page of results.
		entradas = paginator.page(paginator.num_pages)
	return render(request,'planetablogs/index.html',{'user': request.user})
	
	
#Página principal
@login_required()
def index(request):
	return render(request,'planetablogs/index.html',{'user': request.user})



def salir(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))



#Pestaña de puntuaciones de usuarios
@login_required()
def puntuaciones(request):
	lista_usuarios = Alumno.objects.order_by('nombre_apellidos')
	print lista_usuarios
	return render(request, 'planetablogs/puntuaciones.html', {'lista_usuarios':lista_usuarios})



#Pestaña de información de puntuaciones de usuarios
@login_required()
def infopuntuaciones(request):
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(Alumno.objects.all(), ensure_ascii=False)
	return render(request, 'planetablogs/infopuntuaciones.html', {'lista_usuarios':lista_usuarios})



#Dar al botón UP
@login_required()
def up(request):
	lista_entradas = Entrada.objects.order_by('-fecha')
	if request.method=='GET':
		entrada = Entrada.objects.filter(id=request.GET['id'])
		ctx = serializers.serialize('json', entrada, ensure_ascii=False)
		list_entrada = simplejson.loads(ctx)
		json_data = simplejson.dumps( {'entrada':list_entrada} )
	return HttpResponse(json_data, mimetype='application/json')
	
	
	
#Dar al botón DOWN
@login_required()
def down(request):
	lista_entradas = Entrada.objects.order_by('-fecha')
	if request.method=='GET':
		entrada = Entrada.objects.filter(id=request.GET['id'])
		ctx = serializers.serialize('json', entrada, ensure_ascii=False)
		list_entrada = simplejson.loads(ctx)
		json_data = simplejson.dumps( {'entrada':list_entrada} )
	return HttpResponse(json_data, mimetype='application/json')



#Pestaña de búsqueda
@login_required()
def buscar(request):
	return render(request, 'planetablogs/buscar.html')



#Buscar por nick de usuario
@login_required()
def buscarNickUsuario(request):
	if request.method=='GET':
		usu = Alumno.objects.filter(nick=request.GET['texto'])
		entradas = Entrada.objects.filter(usuario=usu)
		json_usuario = serializers.serialize('json', usu, ensure_ascii=False)
		list_usuario = simplejson.loads(json_usuario)
		json_entradas = serializers.serialize('json', entradas, ensure_ascii=False)
		list_entradas = simplejson.loads(json_entradas)
		json_data = simplejson.dumps( {'usuario':list_usuario, 'entradas':list_entradas} )
	return HttpResponse(json_data, mimetype='application/json')



#Buscar por nombre de usuario
@login_required()
def buscarNombreUsuario(request):
	if request.method=='GET':
		usu = Alumno.objects.filter(nombre_apellidos=request.GET['texto'])
		entradas = Entrada.objects.filter(usuario=usu)
		json_usuario = serializers.serialize('json', usu, ensure_ascii=False)
		list_usuario = simplejson.loads(json_usuario)
		json_entradas = serializers.serialize('json', entradas, ensure_ascii=False)
		list_entradas = simplejson.loads(json_entradas)
		json_data = simplejson.dumps( {'usuario':list_usuario, 'entradas':list_entradas} )
	return HttpResponse(json_data, mimetype='application/json')



#Buscar por id de entrada
@login_required()
def buscarIdEntrada(request):
	if request.method=='GET':
		entrada = Entrada.objects.filter(id=request.GET['texto'])
		usuarios = Alumno.objects.all()
		json_usuarios = serializers.serialize('json', usuarios, ensure_ascii=False)
		list_usuarios = simplejson.loads(json_usuarios)
		json_entrada = serializers.serialize('json', entrada, ensure_ascii=False)
		list_entrada = simplejson.loads(json_entrada)
		json_data = simplejson.dumps({'usuarios':list_usuarios, 'entrada':list_entrada} )
	return HttpResponse(json_data, mimetype='application/json')


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
'''