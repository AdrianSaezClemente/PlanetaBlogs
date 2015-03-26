#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from planetablogs.models import Entrada, Alumno, Profesor, Asignatura, Rss, Comentario, Up, Down, Valoracion
from planetablogs.formularios import FormularioRegistro, FormularioIdentidad, FormularioHilo, FormularioAgregarRSS, FormularioAgregarComentario
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
from django.db.models import F
import time
from django.core.serializers.json import DjangoJSONEncoder


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



#Método que actualiza el nivel según la puntuación del alumno en este momento.
def ActualizarNivel(puntos):
	if puntos <= 9:
		nivel = 0
	elif puntos > 9 and puntos <= 24:
		nivel = 1
	elif puntos > 24 and puntos <= 44:
		nivel = 2
	elif puntos > 44 and puntos <= 69:
		nivel = 3
	elif puntos > 69 and puntos <= 99:
		nivel = 4
	elif puntos > 99 and puntos <= 134:
		nivel = 5
	elif puntos > 134 and puntos <= 174:
		nivel = 6
	elif puntos > 174 and puntos <= 219:
		nivel = 7
	elif puntos > 219 and puntos <= 269:
		nivel = 8
	elif puntos > 269 and puntos <= 324:
		nivel = 9
	elif puntos > 324 and puntos <= 384:
		nivel = 10
	elif puntos > 384 and puntos <= 450:
		nivel = 11	
	else:
		nivel = 12
	return nivel



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



#Al llamar a eliminar asignatura del alumno. Se borra todo lo que contenía ese alumno en ese hilo.
def EliminarTodoAlumno(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.delete()
	entradas = Entrada.objects.filter(asignatura_id=idasignatura).filter(alumno_id=idalumno)
	entradas.delete()

	
	
#Eliminar asignatura de los hilos de un alumno
def eliminarasignaturaalumno(request):
	idalumno = ConseguirIdAlumno(request.user.id)
	idasignatura=request.GET['id']
	if request.method=='GET':
		hilo = Rss.objects.get(asignatura=idasignatura,alumno=idalumno)
		hilo.delete()
		EliminarTodoAlumno(idasignatura,idalumno)
		
	return render(request,'planetablogs/presentacionalum.html')



#Método que valida un rss de tal forma que si el enlace rss ya existe en base de datos, el formulario es erróneo.
def ValidarRss(rss):
	lista_rss = Rss.objects.all()
	valido = True
	for i in lista_rss:
		if (rss == i.rss):
			valido = False
			break;
	return valido

	
	
#Muestra la presentación del profesor. Se usa el formulario FormularioAgregarRSS 
#para establecer una relación entre asignatura, alumno y RSS
@login_required()
def presentacionalumno(request):
	info = None
	idasignatura = 0
	idalumno = ConseguirIdAlumno(request.user.id)
	asignaturas = Asignatura.objects.all()
	lista_asignaturas = Asignatura.objects.filter(alumnos=idalumno)
	lista_no_asignaturas = Asignatura.objects.all().exclude(alumnos=idalumno)
	if request.method == 'POST':
		formRSS = FormularioAgregarRSS(request.POST)
		idasignatura = request.POST.get('asignatura', '')
		rss = request.POST.get('rss', '')
		if formRSS.is_valid():
			valido = ValidarRss(rss)
			if valido == True:
				info = False
				hilo = formRSS.save(commit=False)
				hilo.alumno_id = idalumno
				fechaActual = datetime.now()
				hilo.ultima_fecha = fechaActual
				hilo.save()
				#Creo valoración para este usuario en este hilo
				alumno = Alumno.objects.get(id=idalumno)
				asig = Asignatura.objects.get(id=idasignatura)
				valoracion = Valoracion(alumno=alumno,asignatura=asig,puntos=0,nivel=0)
				valoracion.save()
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



#Muestra la presentación del profesor
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


	
#A través del id de la asignatura te devuelve la lista de los alumnos que están inscritos en esa asignatura
def ConseguirListaAlumnos(idasignatura):
	lista_alumno_rss = []
	lista_usuarios = []
	rss = Rss.objects.filter(asignatura_id=idasignatura)
	for i in rss:
		alumno = Alumno.objects.get(id=i.alumno_id)
		lista_alumno_rss = [alumno,i]
		lista_usuarios.append(lista_alumno_rss)
	return lista_usuarios
	


#Comprueba si una entrada (i) está puntuada como UP por un alumno
def ComprobarEntradaPuntuadaUp(i,up,lista_entradas_puntuadas):
	upencontrado = False
	for j in up:
		if i.id == j.entrada_id:
			upencontrado = True
			entrada = [i,True]
			lista_entradas_puntuadas.append(entrada)
			break;
	return upencontrado
	
	
	
#Comprueba si una entrada (i) está puntuada como DOWN por un alumno
def ComprobarEntradaPuntuadaDown(i,down,lista_entradas_puntuadas):
	downencontrado = False
	for j in down:
		if i.id == j.entrada_id:
			downencontrado = True
			entrada = [i,True]
			lista_entradas_puntuadas.append(entrada)
			break;
	return downencontrado



#Obtiene las entradas de un alumno en ese hilo, y si la ha puntuado o no.
def ConseguirListaEntradas(idasignatura,idalumno):
	downencontrado = False
	tupla_entradas = []
	entradas = Entrada.objects.filter(asignatura_id=idasignatura).order_by('-fecha')
	up = Up.objects.filter(alumno_id=idalumno)
	down = Down.objects.filter(alumno_id=idalumno)
	for i in entradas:
		upencontrado = ComprobarEntradaPuntuadaUp(i,up,tupla_entradas)
		downencontrado = ComprobarEntradaPuntuadaDown(i,down,tupla_entradas)
		if (downencontrado == False and upencontrado == False):
			entrada = [i,False]
			tupla_entradas.append(entrada)
	return tupla_entradas


	
#A través del id de la asignatura te devuelve la lista de los ids de los alumnos que están inscritos en esa asignatura
def ConseguirListaComentarios(idasignatura):
	lista_comentarios = Comentario.objects.filter(asignatura_id=idasignatura)
	return lista_comentarios



#Obtener un id de un alumno a través del id como usuario (alumnos más profesores)
def ConseguirIdAlumno(iduser):
	alumno = Alumno.objects.get(alumno_id=iduser)
	return alumno.id
	
	
	
#Se resta 5 puntos al alumno que elimina su propio comentario y actualiza su nivel
def RestarValoracionComentario(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos - 5
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Agrega comentario
def agregarcomentario(request):
	if request.method=='GET':
		descripcion = request.GET['descripcion']
		identrada = request.GET['identrada']
		idalumno = ConseguirIdAlumno(request.GET['iduser'])
		idasignatura = request.GET['idasignatura']
		fecha = datetime.now()
		if descripcion != "":
			comentario = Comentario(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada,fecha=fecha,descripcion=descripcion)
			comentario.save()
			comenta = Comentario.objects.filter(id=comentario.id)
			json_comentario = serializers.serialize('json', comenta, ensure_ascii=False)
			comentario = simplejson.loads(json_comentario)
			usuario = User.objects.filter(id=request.GET['iduser'])
			json_usuario = serializers.serialize('json', usuario, ensure_ascii=False)
			usuario = simplejson.loads(json_usuario)
			json_data = simplejson.dumps( {'comentario':comentario, 'usuario':usuario} )
			SumarValoracionComentario(idasignatura,idalumno)
		else:
			json_data = simplejson.dumps( {'comentario':"", 'usuario':""} )
	return HttpResponse(json_data, mimetype="application/json") 
	


#Elimina comentario
def eliminarcomentario(request):
	if request.method=='GET':
		comentario = Comentario.objects.get(id=request.GET['idcomentario'])
		idasignatura = comentario.asignatura_id
		idalumno = comentario.alumno_id
		comentario.delete()
		RestarValoracionComentario(idasignatura,idalumno)
	return render(request,'planetablogs/index.html',{'user': request.user})
	
	

#Se suma 5 puntos al alumno que hace un comentario y actualiza su nivel
def SumarValoracionComentario(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos + 5
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	

#Página principal de cada hilo en alumnos
@login_required()
def mostrarhiloalumno(request,idasignatura):
	idalumno = ConseguirIdAlumno(request.user.id)
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_usuarios = ConseguirListaAlumnos(idasignatura)
	lista_comentarios = ConseguirListaComentarios(idasignatura)
	lista_entradas_valoradas = Entrada.objects.filter(asignatura_id=idasignatura).order_by('-totalup')[:4]
	tupla_entradas = ConseguirListaEntradas(idasignatura,idalumno)
	
	paginator = Paginator(tupla_entradas, 5) #Muestra 5 entradas por página
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	
		entradas = paginator.page(1)
	except EmptyPage:	
		entradas = paginator.page(paginator.num_pages)

	return render(request,'planetablogs/index.html',{'user': request.user, 'asignatura': asignatura, 'lista_usuarios':lista_usuarios, 'entradas':entradas, 'lista_comentarios':lista_comentarios[::-1], 'lista_entradas_valoradas':lista_entradas_valoradas})



#Página principal de cada hilo en profesores
@login_required()
def mostrarhiloprofesor(request,idasignatura):
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_usuarios = ConseguirListaAlumnos(idasignatura)
	lista_comentarios = ConseguirListaComentarios(idasignatura)
	lista_entradas_valoradas = Entrada.objects.filter(asignatura_id=idasignatura).order_by('-totalup')[:4]
	lista_entradas = Entrada.objects.filter(asignatura_id=idasignatura).order_by('-fecha')
	
	paginator = Paginator(lista_entradas, 5) #Muestra 5 entradas por página
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	
		entradas = paginator.page(1)
	except EmptyPage:	
		entradas = paginator.page(paginator.num_pages)
		
	return render(request,'planetablogs/index_tutor.html',{'user': request.user, 'asignatura': asignatura, 'lista_usuarios':lista_usuarios, 'entradas':entradas, 'lista_comentarios':lista_comentarios[::-1], 'lista_entradas_valoradas':lista_entradas_valoradas})



#Desconectarse de la aplicación
def salir(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))



#Pestaña de puntuaciones de usuarios
@login_required()
def puntuaciones(request,idasignatura):
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_valoracion = Valoracion.objects.filter(asignatura_id=idasignatura).order_by('puntos')
	return render(request, 'planetablogs/puntuaciones.html', {'lista_valoracion':lista_valoracion[::-1], 'user': request.user, 'asignatura': asignatura})



#Pestaña de información de puntuaciones de usuarios
@login_required()
def infopuntuaciones(request,idasignatura):
	asignatura = Asignatura.objects.get(id=idasignatura)
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
	return render(request, 'planetablogs/infopuntuaciones.html', {'lista_usuarios':lista_usuarios, 'user': request.user, 'asignatura': asignatura})
	
	
	
#Suma 1 Up a la entrada y lo guarda
def GuardarUp(identrada):
	entrada = Entrada.objects.get(id=identrada)
	entrada.totalup = entrada.totalup + 1
	entrada.save()
	


#A un alumno de una asignatura, se le suma al total de puntos, 3 puntos por darle al botón UP y actualiza su nivel
def SumarValoracionUp(idasignatura,idalumno,identrada):
	entrada = Entrada.objects.get(id=identrada)
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=entrada.alumno_id)
	val.puntos = val.puntos + 3
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Dar al botón UP
@login_required()
def up(request):
	if request.method=='GET':
		print "he dado al up"
		idasignatura = request.GET['idasignatura']
		idalumno = ConseguirIdAlumno(request.GET['idusuario'])
		identrada = request.GET['identrada']
		total=request.GET['up']
		up = Up(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada)
		up.save()
		GuardarUp(identrada)
		SumarValoracionUp(idasignatura,idalumno,identrada)
	return render(request,'planetablogs/index.html',{'user': request.user})
	
	
	
#Suma 1 Down a la entrada y lo guarda
def GuardarDown(identrada):
	entrada = Entrada.objects.get(id=identrada)
	entrada.totaldown = entrada.totaldown + 1
	entrada.save()
	
	

#A un alumno de una asignatura, se le resta al total de puntos, 1 puntos por darle al botón DOWN y actualiza su nivel
def RestarValoracionDown(idasignatura,idalumno,identrada):
	entrada = Entrada.objects.get(id=identrada)
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=entrada.alumno_id)
	val.puntos = val.puntos - 1
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Dar al botón DOWN
@login_required()
def down(request):
	if request.method=='GET':
		print "he dado al down"
		idasignatura = request.GET['idasignatura']
		idalumno = ConseguirIdAlumno(request.GET['idusuario'])
		identrada = request.GET['identrada']
		total=request.GET['down']
		down = Down(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada)
		down.save()
		GuardarDown(identrada)
		RestarValoracionDown(idasignatura,idalumno,identrada)
	return render(request,'planetablogs/index.html',{'user': request.user})



#Pestaña de búsqueda
@login_required()
def buscar(request,idasignatura):
	asignatura = Asignatura.objects.get(id=idasignatura)
	return render(request,'planetablogs/buscar.html',{'user': request.user, 'asignatura': asignatura})



#Buscar por nick de usuario
@login_required()
def buscarNickUsuario(request):
	if request.method=='GET':
		if request.GET['texto'] != "":
			usu = User.objects.filter(username=request.GET['texto'])
			if len(usu) != 0:
				idalumno = ConseguirIdAlumno(usu)
				entradas = Entrada.objects.filter(alumno_id=idalumno)
				json_usuario = serializers.serialize('json', usu, ensure_ascii=False)
				list_usuario = simplejson.loads(json_usuario)
				json_entradas = serializers.serialize('json', entradas, ensure_ascii=False)
				list_entradas = simplejson.loads(json_entradas)
				json_data = simplejson.dumps( {'usuario':list_usuario, 'entradas':list_entradas} )
			else:
				json_data = simplejson.dumps( {'usuario':"", 'entradas':[]} )
		else:
			json_data = simplejson.dumps( {'usuario':"", 'entradas':""} )
	return HttpResponse(json_data, mimetype='application/json')



#Buscar por nombre de usuario
@login_required()
def buscarNombreUsuario(request):
	if request.method=='GET':
		if request.GET['texto'] != "":
			usu = User.objects.filter(first_name=request.GET['texto'])
			if len(usu) != 0:
				idalumno = ConseguirIdAlumno(usu)
				entradas = Entrada.objects.filter(alumno_id=idalumno)
				json_usuario = serializers.serialize('json', usu, ensure_ascii=False)
				list_usuario = simplejson.loads(json_usuario)
				json_entradas = serializers.serialize('json', entradas, ensure_ascii=False)
				list_entradas = simplejson.loads(json_entradas)
				json_data = simplejson.dumps( {'usuario':list_usuario, 'entradas':list_entradas} )
			else:
				json_data = simplejson.dumps( {'usuario':"", 'entradas':[]} )
		else:
			json_data = simplejson.dumps( {'usuario':"", 'entradas':""} )
	return HttpResponse(json_data, mimetype='application/json')



#Buscar por id de entrada
@login_required()
def buscarIdEntrada(request):
	if request.method=='GET':
		if request.GET['texto'] != "":
			entrada = Entrada.objects.filter(id=request.GET['texto'])
			if len(entrada) != 0:
				alumno = Alumno.objects.filter(id=entrada[0].alumno_id)
				user = User.objects.filter(id=alumno[0].alumno.id)
				json_usuario = serializers.serialize('json', user, ensure_ascii=False)
				list_usuario = simplejson.loads(json_usuario)
				json_entrada = serializers.serialize('json', entrada, ensure_ascii=False)
				list_entrada = simplejson.loads(json_entrada)
				json_data = simplejson.dumps({'usuario':list_usuario, 'entrada':list_entrada} )
			else:
				json_data = simplejson.dumps( {'usuario':"", 'entrada':""} )
		else:
			json_data = simplejson.dumps( {'alumno':"", 'entrada':""} )
	return HttpResponse(json_data, mimetype='application/json')


if __name__ == '__main__':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFG.settings")
