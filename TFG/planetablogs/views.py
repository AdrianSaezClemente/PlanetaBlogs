#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from planetablogs.models import Entrada, Alumno, Profesor, Asignatura, Rss, Comentario, Up, Down, Valoracion
from planetablogs.formularios import FormularioResetPasswd, FormularioRegistro, FormularioIdentidad, FormularioHilo, FormularioAgregarRSS, FormularioAgregarComentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import feedparser
from time import mktime
from datetime import datetime
from dateutil import tz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.utils import simplejson
from django.contrib import auth
from django.db.models import F
import time
from django.core.serializers.json import DjangoJSONEncoder
import sys
	
def mierror404(request):
	print "error404"
	return render(request, 'planetablogs/error404.html')



#Introducir datos de registro de alumno
def nuevo_alumno(request):
	ficheroNohup = open('nohup.out', 'a')
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
	info = True
	if request.method == 'POST':
		form = FormularioRegistro(request.POST, request.FILES)
		if form.is_valid():
			info = True
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			imagen = form.cleaned_data["imagen"]
			
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.imagen = imagen
			user.save()
			
			alum = Alumno(alumno=user)
			alum.save()
			ficheroNohup.write("[**NA**] Alumno "+user.username.encode('utf-8')+" registrado con éxito.\n")
			#print "[****] Alumno "+user.username.encode('utf-8')+" registrado con éxito."
			return HttpResponseRedirect(reverse('login'))  # Redirect after POST
		else:
			ficheroNohup.write("[**FR**] Alumno registrado sin éxito.\n")
			#print "[****] Alumno registrado sin éxito."
			info = False
			return render(request, 'planetablogs/nuevoalumno.html', {'info': info, 'json_usuarios': json_usuarios})
	else:
		form = FormularioRegistro()
	ficheroNohup.close()
	return render(request, 'planetablogs/nuevoalumno.html', {'info': info, 'json_usuarios': json_usuarios})



#Introducir datos de registro de profesor
def nuevo_profesor(request):
	ficheroNohup = open('nohup.out', 'a')
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
	info = True
	if request.method == 'POST':
		form = FormularioRegistro(request.POST, request.FILES)
		if form.is_valid():
			info = True
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			imagen = form.cleaned_data["imagen"]
			
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.imagen = imagen
			user.save()
			profe = Profesor(profesor=user)
			profe.save()
			ficheroNohup.write("[**NT**] Tutor "+user.username.encode('utf-8')+" registrado con éxito.\n")
			#print "[****] Tutor "+user.username.encode('utf-8')+" registrado con éxito."
			return HttpResponseRedirect(reverse('login'))  # Redirect after POST
		else:
			ficheroNohup.write("[**FR**] Tutor registrado sin éxito.\n")
			#print "[****] Tutor registrado sin éxito."
			info = False
			return render(request, 'planetablogs/nuevoprofesor.html', {'info': info, 'json_usuarios': json_usuarios})
	else:
		form = FormularioRegistro()
	ficheroNohup.close()
	return render(request, 'planetablogs/nuevoprofesor.html', {'info': info, 'json_usuarios': json_usuarios})



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
	ficheroNohup = open('nohup.out', 'a')
	error = None
	try:
		if request.method == 'POST':
			ficheroNohup.write("Inicio de aplicación\n")
			username = request.POST.get('nick', '')
			password = request.POST.get('password', '')
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				error = False
				auth.login(request, user)
				request.session['usuario_conectado'] = user.id
				request.session['conectado'] = True
				usuario = ComprobarUsuario(user.id)
				if (usuario == "Alumno"):
					ficheroNohup.write("[**IA**] Alumno "+request.user.username.encode('utf-8')+" identificado con éxito.\n")
					return HttpResponseRedirect(reverse('presentacionalumno'))
				else:
					ficheroNohup.write("[**IT**] Tutor "+request.user.username.encode('utf-8')+" identificado con éxito.\n")
					return HttpResponseRedirect(reverse('presentacionprofesor'))
			else:
				error = True
				return render(request, 'planetablogs/inicio.html', {'login': error})
		if request.session['usuario_conectado'] == request.user.id:
			usuario = ComprobarUsuario(request.user.id)
			if (usuario == "Alumno"):
				ficheroNohup.write("[**SLA**] Alumno "+request.user.username.encode('utf-8')+" identificado sin logout.\n")
				#print "[****] Alumno "+request.user.username.encode('utf-8')+" identificado sin logout."
				return HttpResponseRedirect(reverse('presentacionalumno'))
			else:
				ficheroNohup.write("[**SLT**] Tutor "+request.user.username.encode('utf-8')+" identificado sin logout.\n")
				#print "[****] Tutor "+request.user.username.encode('utf-8')+" identificado sin logout."
				return HttpResponseRedirect(reverse('presentacionprofesor'))
	except KeyError:
		pass
	ficheroNohup.close()
	return render(request, 'planetablogs/inicio.html', {'login': error})



#Al llamar a eliminar asignatura del alumno. Se borra todo lo que contenía ese alumno en ese hilo.
def EliminarTodoAlumno(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.delete()
	entradas = Entrada.objects.filter(asignatura_id=idasignatura).filter(alumno_id=idalumno)
	entradas.delete()

	
	
#Eliminar asignatura de los hilos de un alumno
def eliminarasignaturaalumno(request):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	idasignatura=request.GET['id']
	if request.method=='GET':
		hilo = Rss.objects.get(asignatura=idasignatura,alumno=idalumno)
		hilo.delete()
		ficheroNohup.write("[**EAA**] Alumno "+request.user.username.encode('utf-8')+" elimina hilo "+ idasignatura.encode('utf-8') +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" elimina hilo", idasignatura
		EliminarTodoAlumno(idasignatura,idalumno)
	ficheroNohup.close()
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
	ficheroNohup = open('nohup.out', 'a')
	ficheroNohup.write("Inicio de presentación de alumno\n")
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
				from_zone = tz.tzutc()
				utc = fechaActual.replace(tzinfo=from_zone)
				utc_str = utc.strftime("%Y-%m-%d %H:%M:%S")
				hilo.ultima_fecha = utc_str
				hilo.save()
				#Creo valoración para este usuario en este hilo
				alumno = Alumno.objects.get(id=idalumno)
				asig = Asignatura.objects.get(id=idasignatura)
				ficheroNohup.write("[**SHA**] Alumno "+request.user.username.encode('utf-8')+" suscrito a hilo "+ str(asig) +"\n")
				valoracion = Valoracion(alumno=alumno,asignatura=asig,puntos=0,nivel=0)
				valoracion.save()
			else:
				info = True
		else:
			info = True
	ficheroNohup.close()
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
	ficheroNohup = open('nohup.out', 'a')
	ficheroNohup.write("Inicio de presentación de profesor\n")
	asignaturas = Asignatura.objects.all()
	lista_asignaturas = Asignatura.objects.filter(profesores=request.user.id)
	lista_no_asignaturas = Asignatura.objects.all().exclude(profesores=request.user.id)
	if request.method == 'POST':
		formHilo = FormularioHilo(request.POST)
		if formHilo.is_valid():
			hilo = formHilo.save(commit=False)
			hilo.entradas = 0
			hilo.creador = request.user.id
			hilo.save()
			return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})
		else:
			print "NO VALIDO formHilo"
	ficheroNohup.close()
	return render(request,'planetablogs/presentacionprof.html',{'user': request.user, 'lista_asignaturas': lista_asignaturas, 'lista_no_asignaturas': lista_no_asignaturas, 'asignaturas': asignaturas})


	
#A través del id de la asignatura te devuelve la lista de los alumnos que están inscritos en esa asignatura
def ConseguirListaAlumnos(idasignatura):
	lista_alumno_rss = []
	lista_usuarios = []
	rss = Rss.objects.filter(asignatura_id=idasignatura)
	for i in rss:
		alumno = Alumno.objects.get(id=i.alumno_id)
		if alumno.alumno.username != "admin":
			lista_alumno_rss = [alumno,i]
			lista_usuarios.append(lista_alumno_rss)
	return lista_usuarios
	


#Devuelve el total de comentarios de un alumno dados
def ConseguirTotalComentariosDados(idalumno,idasignatura):
	totalComentariosDados = 0
	comentarios = Comentario.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for comen in comentarios:
		totalComentariosDados = totalComentariosDados + 1
	return totalComentariosDados



#Devuelve el total de comentarios de un alumno recibidos
def ConseguirTotalComentariosRecibidos(idalumno,idasignatura):
	totalComentariosRecibidos = 0
	entradas = Entrada.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for ent in entradas:
		totalComentariosRecibidos = totalComentariosRecibidos + ent.totalcomentarios
	return totalComentariosRecibidos



#Devuelve el total de down de un alumno dados
def ConseguirTotalDownDados(idalumno,idasignatura):
	totalDownDados = 0
	downs = Down.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for down in downs:
		totalDownDados = totalDownDados + 1
	return totalDownDados



#Devuelve el total de up de un alumno dados
def ConseguirTotalUpDados(idalumno,idasignatura):
	totalUpDados = 0
	ups = Up.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for up in ups:
		totalUpDados = totalUpDados + 1
	return totalUpDados



#Devuelve el total de up de un alumno recibidos
def ConseguirTotalUpRecibidos(idalumno,idasignatura):
	totalUpRecibidos = 0
	entradas = Entrada.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for ent in entradas:
		totalUpRecibidos = totalUpRecibidos + ent.totalup
	return totalUpRecibidos



#Devuelve el total de down de un alumno recibidos
def ConseguirTotalDownRecibidos(idalumno,idasignatura):
	totalDownRecibidos = 0
	entradas = Entrada.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for ent in entradas:
		totalDownRecibidos = totalDownRecibidos + ent.totaldown
	return totalDownRecibidos



#Devuelve el total de las entradas de un alumno
def ConseguirTotalEntradas(idalumno,idasignatura):
	total = 0
	entradas = Entrada.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
	for ent in entradas:
		total = total + 1
	return total
		
		
		
#A través del id de la asignatura te devuelve la lista de alumnos con el total de entradas de cada uno.
def ConseguirTotalEntradasUsuario(idasignatura):
	lista_alumno_totalentradas = []
	lista_usuario_totalentradas = []
	rss = Rss.objects.filter(asignatura_id=idasignatura)
	for i in rss:
		alumno = Alumno.objects.get(id=i.alumno_id)
		if alumno.alumno.username != "admin":
			totalentradas = ConseguirTotalEntradas(alumno.id,idasignatura)
			totalUpRecibidos = ConseguirTotalUpRecibidos(alumno.id,idasignatura)
			totalDownRecibidos = ConseguirTotalDownRecibidos(alumno.id,idasignatura)
			totalUpDados = ConseguirTotalUpDados(alumno.id,idasignatura)
			totalDownDados = ConseguirTotalDownDados(alumno.id,idasignatura)
			totalComentariosRecibidos = ConseguirTotalComentariosRecibidos(alumno.id,idasignatura)
			totalComentariosDados = ConseguirTotalComentariosDados(alumno.id,idasignatura)
			lista_alumno_totalentradas = [alumno,totalentradas,totalUpRecibidos,totalDownRecibidos,totalUpDados,totalDownDados,totalComentariosRecibidos,totalComentariosDados]
			lista_usuario_totalentradas.append(lista_alumno_totalentradas)
	return lista_usuario_totalentradas



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
	
	
	
#Se resta 3 puntos al alumno que elimina su propio comentario y actualiza su nivel
def RestarValoracionComentario(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos - 3
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
def SumarComentarioEntrada(idasignatura,identrada):
	entrada = Entrada.objects.get(id=identrada,asignatura_id=idasignatura)
	entrada.totalcomentarios = entrada.totalcomentarios + 1
	entrada.save()
	
	

#Agrega comentario
def agregarcomentario(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		descripcion = request.GET['descripcion']
		identrada = request.GET['identrada']
		idalumno = ConseguirIdAlumno(request.GET['iduser'])
		idasignatura = request.GET['idasignatura']
		usuario = User.objects.get(id=request.GET['iduser'])
		username = usuario.username
		fecha = datetime.now()
		if descripcion != "":
			comentario = Comentario(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada,fecha=fecha,descripcion=descripcion,username=username)
			comentario.save()
			comenta = Comentario.objects.filter(id=comentario.id)
			json_comentario = serializers.serialize('json', comenta, ensure_ascii=False)
			comentario = simplejson.loads(json_comentario)
			json_data = simplejson.dumps( {'comentario':comentario} )
			SumarValoracionComentario(idasignatura,idalumno)
			SumarComentarioEntrada(idasignatura,identrada)
			ficheroNohup.write("[**AAC**] Alumno "+username.encode('utf-8')+" agrega comentario a entrada "+ identrada.encode('utf-8') +"\n")
			#print "[****] Alumno "+username.encode('utf-8')+" agrega comentario a entrada", identrada
		else:
			json_data = simplejson.dumps( {'comentario':""} )
	ficheroNohup.close()
	return HttpResponse(json_data, mimetype="application/json") 
	


def RestarComentarioEntrada(idasignatura,identrada):
	entrada = Entrada.objects.get(id=identrada,asignatura_id=idasignatura)
	entrada.totalcomentarios = entrada.totalcomentarios - 1
	entrada.save()
	
	
	
#Elimina comentario
def eliminarcomentario(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		identrada = request.GET['identrada']
		comentario = Comentario.objects.get(id=request.GET['idcomentario'])
		idasignatura = comentario.asignatura_id
		idalumno = comentario.alumno_id
		comentario.delete()
		RestarValoracionComentario(idasignatura,idalumno)
		RestarComentarioEntrada(idasignatura,identrada)
		ficheroNohup.write("[**CE**] Comentario de "+comentario.username.encode('utf-8')+" eliminado en entrada "+ identrada.encode('utf-8') +"\n")
		#print "[****] Comentario de "+comentario.username.encode('utf-8')+" eliminado en entrada", identrada
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'user': request.user})
	
	

#Se suma 3 puntos al alumno que hace un comentario y actualiza su nivel
def SumarValoracionComentario(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos + 3
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()



#Resta la valoración de la entrada al alumno que escribió la entrada eliminada
def RestarValoracionEntrada(idasignatura,idalumno):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos - 10
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Recalcula el total de puntos obtenidos en cada entrada
def RecalcularTotalEntrada(identrada,contadorUp,contadorDown):
	entrada = Entrada.objects.get(id=identrada)
	entrada.total = entrada.total + contadorDown - (2*contadorUp)
	entrada.save()
	
	
	
#Suma y resta la valoración de ups y downs al alumno que escribió la entrada eliminada
def RecalcularValoracionUpDown(identrada,idasignatura,idalumno,contadorUp,contadorDown):
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
	val.puntos = val.puntos + contadorDown - (2*contadorUp)
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	RecalcularTotalEntrada(identrada,contadorUp,contadorDown)
	
	
	
#Elimina los Ups, los Downs que hay en la entrada eliminada
def EliminarUpDown(idasignatura,identrada,idalumno):
	contadorUp = 0
	contadorDown = 0
	ups = Up.objects.filter(asignatura_id=idasignatura,entrada_id=identrada)
	downs = Down.objects.filter(asignatura_id=idasignatura,entrada_id=identrada)
	for up in ups:
		contadorUp = contadorUp + 1
		up.delete()
	for down in downs:
		contadorDown = contadorDown + 1
		down.delete()
	RecalcularValoracionUpDown(identrada,idasignatura,idalumno,contadorUp,contadorDown)
	
	
	
#Elimina entrada de un hilo
def eliminarentrada(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		idasignatura = request.GET['idasignatura']
		identrada = request.GET['identrada']
		entrada = Entrada.objects.get(id=identrada)
		idalumno = entrada.alumno.id
		EliminarUpDown(idasignatura,identrada,idalumno)#Elimino Ups y Downs, y recalculo valoración de alumno
		entrada.delete()#Elimino Entrada, y recalculo valoración de alumno
		RestarValoracionEntrada(idasignatura,idalumno)
		ficheroNohup.write("[**EET**] Tutor "+request.user.username.encode('utf-8')+" elimina entrada "+ identrada.encode('utf-8') +"\n")
		#print "[****] Tutor "+request.user.username.encode('utf-8')+" elimina entrada", identrada
		#FALTA RECALCULAR ELIMINAR COMENTARIOS DE LA ENTRADA ELIMINADA--------------------------------------------------------------------
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'user': request.user})



#Elimina alumno de un hilo
def eliminaralumno(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		idasignatura = request.GET['idasignatura']
		iduser = request.GET['idalumno']
		idalumno = ConseguirIdAlumno(iduser)
		rss = Rss.objects.filter(asignatura_id=idasignatura,alumno_id=idalumno)
		rss.delete()
		EliminarTodoAlumno(idasignatura,idalumno)
		ficheroNohup.write("[**EAT**] Tutor "+request.user.username.encode('utf-8')+" elimina alumno "+ str(idalumno) +"\n")
		#print "[****] Tutor "+request.user.username.encode('utf-8')+" elimina alumno", idalumno
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'user': request.user})



#Vista que comprueba si un usuario está suscrito a una asignatura
def ComprobarUsuarioAsignatura(idasignatura,idalumno):
	suscrito = False
	rss = Rss.objects.filter(asignatura_id=idasignatura)
	for i in rss:
		if i.alumno_id == idalumno:
			suscrito = True
			break;
	return suscrito



#Página principal de cada hilo en alumnos
@login_required()
def mostrarhiloalumno(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
		lista_usuarios = ConseguirListaAlumnos(idasignatura)
		lista_comentarios = ConseguirListaComentarios(idasignatura)
		#CAMBIAR SI NO HAY ADMIN (Quitar exclude)
		lista_entradas_valoradas = Entrada.objects.filter(asignatura_id=idasignatura).exclude(alumno_id=1).order_by('-total')[:10]
		tupla_entradas = ConseguirListaEntradas(idasignatura,idalumno)

		json_serializer = serializers.get_serializer("json")()
		json_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
		json_valoracion = json_serializer.serialize(Valoracion.objects.filter(asignatura_id=idasignatura), ensure_ascii=False)
		json_alumnos = json_serializer.serialize(Alumno.objects.all(), ensure_ascii=False)
		json_asignaturas = json_serializer.serialize(Asignatura.objects.all(), ensure_ascii=False)
		json_profesores = json_serializer.serialize(Profesor.objects.all(), ensure_ascii=False)
		
		ficheroNohup.write("[**VHA**] Alumno "+request.user.username.encode('utf-8')+" visita hilo "+ str(asignatura) +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" visita hilo", asignatura
		paginator = Paginator(tupla_entradas, 5) #Muestra 5 entradas por página
		page = request.GET.get('page')
		try:
			entradas = paginator.page(page)
		except PageNotAnInteger:	
			entradas = paginator.page(1)
		except EmptyPage:	
			entradas = paginator.page(paginator.num_pages)
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'json_profesores':json_profesores, 'json_asignaturas':json_asignaturas, 'json_alumnos':json_alumnos, 'json_valoracion':json_valoracion, 'json_usuarios':json_usuarios, 'user': request.user, 'asignatura': asignatura, 'lista_usuarios':lista_usuarios, 'entradas':entradas, 'lista_comentarios':lista_comentarios[::-1], 'lista_entradas_valoradas':lista_entradas_valoradas})



#Página principal de cada hilo en profesores
@login_required()
def mostrarhiloprofesor(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_usuarios = ConseguirListaAlumnos(idasignatura)
	lista_comentarios = ConseguirListaComentarios(idasignatura)
	#CAMBIAR SI NO HAY ADMIN (Quitar exclude)
	lista_entradas_valoradas = Entrada.objects.filter(asignatura_id=idasignatura).exclude(alumno_id=1).order_by('-total')[:10]
	lista_entradas = Entrada.objects.filter(asignatura_id=idasignatura).order_by('-fecha')

	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
	json_valoracion = json_serializer.serialize(Valoracion.objects.filter(asignatura_id=idasignatura), ensure_ascii=False)
	json_alumnos = json_serializer.serialize(Alumno.objects.all(), ensure_ascii=False)
	json_asignaturas = json_serializer.serialize(Asignatura.objects.all(), ensure_ascii=False)
	json_profesores = json_serializer.serialize(Profesor.objects.all(), ensure_ascii=False)
	
	ficheroNohup.write("[**VHT**] Tutor "+request.user.username.encode('utf-8')+" visita hilo "+ str(asignatura) +"\n")
	#print "[****] Tutor "+request.user.username.encode('utf-8')+" visita hilo", asignatura
	paginator = Paginator(lista_entradas, 5) #Muestra 5 entradas por página
	page = request.GET.get('page')
	try:
		entradas = paginator.page(page)
	except PageNotAnInteger:	
		entradas = paginator.page(1)
	except EmptyPage:	
		entradas = paginator.page(paginator.num_pages)
	ficheroNohup.close()
	return render(request,'planetablogs/index_tutor.html',{'json_profesores':json_profesores, 'json_asignaturas':json_asignaturas, 'json_alumnos':json_alumnos, 'json_valoracion':json_valoracion, 'json_usuarios':json_usuarios, 'user': request.user, 'asignatura': asignatura, 'lista_usuarios':lista_usuarios, 'entradas':entradas, 'lista_comentarios':lista_comentarios[::-1], 'lista_entradas_valoradas':lista_entradas_valoradas})



#Desconectarse de la aplicación
def salir(request):
	ficheroNohup = open('nohup.out', 'a')
	try:
		username = request.user
		logout(request)
		ficheroNohup.write("[**LU**] Usuario "+ str(username) +" ha salido de la aplicación.\n")
		#print "[****] Usuario", username ,"ha salido de la aplicación."
	except KeyError:
		pass
	ficheroNohup.close()
	return HttpResponseRedirect(reverse('login'))



#Pestaña de puntuaciones de usuarios
@login_required()
def puntuaciones(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
		lista_valoracion = Valoracion.objects.filter(asignatura_id=idasignatura).order_by('puntos').exclude(alumno_id=1)
		json_serializer = serializers.get_serializer("json")()
		json_usuarios = json_serializer.serialize(User.objects.all().exclude(username="admin"), ensure_ascii=False)
		ficheroNohup.write("[**VRA**] Alumno "+request.user.username.encode('utf-8')+" visita RANKING de "+ str(asignatura) +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" visita RANKING de", asignatura
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	ficheroNohup.close()
	return render(request, 'planetablogs/puntuaciones.html', {'json_usuarios':json_usuarios, 'lista_valoracion':lista_valoracion[::-1], 'user': request.user, 'asignatura': asignatura})



#Pestaña de estadísticas de usuarios
@login_required()
def estadisticas(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
		lista_usuario_totalentradas = ConseguirTotalEntradasUsuario(idasignatura)
		entradas = Entrada.objects.filter(asignatura_id=idasignatura)
		ficheroNohup.write("[**VEA**] Alumno "+request.user.username.encode('utf-8')+" visita ESTADISTICAS de "+ str(asignatura) +"\n")
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	ficheroNohup.close()
	return render(request, 'planetablogs/estadisticas.html', {'entradas':entradas[::-1], 'user': request.user, 'asignatura': asignatura, 'lista_usuario_totalentradas':lista_usuario_totalentradas})



#Pestaña de información de puntuaciones de usuarios
@login_required()
def infopuntuaciones(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
		json_serializer = serializers.get_serializer("json")()
		lista_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
		ficheroNohup.write("[**VIA**] Alumno "+request.user.username.encode('utf-8')+" visita INFOPUNTUACIONES de "+ str(asignatura) +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" visita INFOPUNTUACIONES de", asignatura
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	ficheroNohup.close()
	return render(request, 'planetablogs/infopuntuaciones.html', {'lista_usuarios':lista_usuarios, 'user': request.user, 'asignatura': asignatura})
	
	
	
#Suma 1 Up a la entrada y lo guarda
def GuardarUp(identrada):
	entrada = Entrada.objects.get(id=identrada)
	entrada.totalup = entrada.totalup + 1
	entrada.total = entrada.total + 2
	entrada.save()
	


#A un alumno de una asignatura, se le suma al total de puntos, 2 puntos por darle al botón UP y actualiza su nivel
def SumarValoracionUp(idasignatura,idalumno,identrada):
	entrada = Entrada.objects.get(id=identrada)
	val = Valoracion.objects.get(asignatura=idasignatura,alumno=entrada.alumno_id)
	val.puntos = val.puntos + 2
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Dar al botón UP
@login_required()
def up(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		idasignatura = request.GET['idasignatura']
		idalumno = ConseguirIdAlumno(request.GET['idusuario'])
		identrada = request.GET['identrada']
		total=request.GET['up']
		up = Up(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada)
		up.save()
		GuardarUp(identrada)
		SumarValoracionUp(idasignatura,idalumno,identrada)
		ficheroNohup.write("[**PU**] Alumno "+request.user.username.encode('utf-8')+" pulsa UP en entrada "+ identrada.encode('utf-8') +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" pulsa UP en entrada", identrada
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'user': request.user})
	
	
	
#Suma 1 Down a la entrada y lo guarda
def GuardarDown(identrada):
	entrada = Entrada.objects.get(id=identrada)
	entrada.totaldown = entrada.totaldown + 1
	entrada.total = entrada.total - 1
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
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		idasignatura = request.GET['idasignatura']
		idalumno = ConseguirIdAlumno(request.GET['idusuario'])
		identrada = request.GET['identrada']
		total=request.GET['down']
		down = Down(asignatura_id=idasignatura,alumno_id=idalumno,entrada_id=identrada)
		down.save()
		GuardarDown(identrada)
		RestarValoracionDown(idasignatura,idalumno,identrada)
		ficheroNohup.write("[**PD**] Alumno "+request.user.username.encode('utf-8')+" pulsa DOWN en entrada "+ identrada.encode('utf-8') +"\n")
		#print "[****] Alumno "+request.user.username.encode('utf-8')+" pulsa DOWN en entrada", identrada
	ficheroNohup.close()
	return render(request,'planetablogs/index.html',{'user': request.user})



#Pestaña de búsqueda
@login_required()
def buscar(request,idasignatura):
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	return render(request,'planetablogs/buscar.html',{'user': request.user, 'asignatura': asignatura})



#Pestaña de ayuda
def ayuda(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	idalumno = ConseguirIdAlumno(request.user.id)
	suscrito = ComprobarUsuarioAsignatura(idasignatura,idalumno)
	if suscrito == True:
		asignatura = Asignatura.objects.get(id=idasignatura)
		ficheroNohup.write("[**AYA**] Alumno "+request.user.username.encode('utf-8')+" visita AYUDA de "+ str(asignatura) +"\n")
	else:
		return HttpResponseRedirect(reverse('presentacionalumno'))
	ficheroNohup.close()
	return render(request,'planetablogs/ayuda.html',{'user': request.user, 'asignatura': asignatura})



#Pestaña de búsqueda en tutores
@login_required()
def buscar_tutor(request,idasignatura):
	asignatura = Asignatura.objects.get(id=idasignatura)
	return render(request,'planetablogs/buscar_tutor.html',{'user': request.user, 'asignatura': asignatura})



#Pestaña de ayuda en tutores
def ayuda_tutor(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	asignatura = Asignatura.objects.get(id=idasignatura)
	ficheroNohup.write("[**AYT**] Alumno "+request.user.username.encode('utf-8')+" visita AYUDA de "+ str(asignatura) +"\n")
	ficheroNohup.close()
	return render(request,'planetablogs/ayuda_tutor.html',{'user': request.user, 'asignatura': asignatura})



#Pestaña de puntuaciones de usuarios en tutores
@login_required()
def puntuaciones_tutor(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_valoracion = Valoracion.objects.filter(asignatura_id=idasignatura).order_by('puntos').exclude(alumno_id=1)
	json_serializer = serializers.get_serializer("json")()
	json_usuarios = json_serializer.serialize(User.objects.all().exclude(username="admin"), ensure_ascii=False)
	ficheroNohup.write("[**VRT**] Tutor "+request.user.username.encode('utf-8')+" visita RÁNKING de "+ str(asignatura) +"\n")
	#print "[****] Tutor "+request.user.username.encode('utf-8')+" visita RÁNKING de", asignatura
	ficheroNohup.close()
	return render(request, 'planetablogs/puntuaciones_tutor.html', {'json_usuarios':json_usuarios, 'lista_valoracion':lista_valoracion[::-1], 'user': request.user, 'asignatura': asignatura})



#Pestaña de estadísticas de usuarios en tutores
@login_required()
def estadisticas_tutor(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	asignatura = Asignatura.objects.get(id=idasignatura)
	lista_usuario_totalentradas = ConseguirTotalEntradasUsuario(idasignatura)
	entradas = Entrada.objects.filter(asignatura_id=idasignatura)
	ficheroNohup.write("[**VET**] Tutor "+request.user.username.encode('utf-8')+" visita ESTADISTICAS de "+ str(asignatura) +"\n")
	ficheroNohup.close()
	return render(request, 'planetablogs/estadisticas_tutor.html', {'entradas':entradas[::-1], 'user': request.user, 'asignatura': asignatura, 'lista_usuario_totalentradas':lista_usuario_totalentradas})



#Pestaña de información de puntuaciones de usuarios en tutores
@login_required()
def infopuntuaciones_tutor(request,idasignatura):
	ficheroNohup = open('nohup.out', 'a')
	asignatura = Asignatura.objects.get(id=idasignatura)
	json_serializer = serializers.get_serializer("json")()
	lista_usuarios = json_serializer.serialize(User.objects.all(), ensure_ascii=False)
	ficheroNohup.write("[**VIT**] Tutor "+request.user.username.encode('utf-8')+" visita INFOPUNTUACIONES de "+ str(asignatura) +"\n")
	#print "[****] Tutor "+request.user.username.encode('utf-8')+" visita INFOPUNTUACIONES de", asignatura
	ficheroNohup.close()
	return render(request, 'planetablogs/infopuntuaciones_tutor.html', {'lista_usuarios':lista_usuarios, 'user': request.user, 'asignatura': asignatura})
	
	
	
#Buscar por nick de usuario
@login_required()
def buscarNickUsuario(request):
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		if request.GET['texto'] != "":
			usu = User.objects.filter(username=request.GET['texto'])
			idasignatura = request.GET['idasignatura']
			if len(usu) != 0:
				idalumno = ConseguirIdAlumno(usu)
				entradas = Entrada.objects.filter(alumno_id=idalumno).filter(asignatura_id=idasignatura)
				comentarios = ConseguirListaComentarios(idasignatura)
				json_usuario = serializers.serialize('json', usu, ensure_ascii=False)
				list_usuario = simplejson.loads(json_usuario)
				json_entradas = serializers.serialize('json', entradas, ensure_ascii=False)
				list_entradas = simplejson.loads(json_entradas)
				json_comentarios = serializers.serialize('json', comentarios, ensure_ascii=False)
				list_comentarios = simplejson.loads(json_comentarios)
				json_data = simplejson.dumps( {'usuario':list_usuario, 'entradas':list_entradas, 'comentarios':list_comentarios} )
				ficheroNohup.write("[**BNU**] Búsqueda de "+request.user.username.encode('utf-8')+" por nick de usuario "+ request.GET['texto'].encode('utf-8') +"\n")
				#print "[****] Búsqueda de "+request.user.username.encode('utf-8')+" por nick de usuario", request.GET['texto']
			else:
				json_data = simplejson.dumps( {'usuario':"", 'entradas':[], 'comentarios':[]} )
		else:
			json_data = simplejson.dumps( {'usuario':"", 'entradas':"", 'comentarios':[]} )
	ficheroNohup.close()
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
	ficheroNohup = open('nohup.out', 'a')
	if request.method=='GET':
		if request.GET['texto'] != "":
			idasignatura = request.GET['idasignatura']
			entrada = Entrada.objects.filter(entrada=request.GET['texto']).filter(asignatura_id=idasignatura)
			if len(entrada) != 0:
				alumno = Alumno.objects.filter(id=entrada[0].alumno_id)
				user = User.objects.filter(id=alumno[0].alumno.id)
				comentarios = ConseguirListaComentarios(idasignatura)
				json_usuario = serializers.serialize('json', user, ensure_ascii=False)
				list_usuario = simplejson.loads(json_usuario)
				json_entrada = serializers.serialize('json', entrada, ensure_ascii=False)
				list_entrada = simplejson.loads(json_entrada)
				json_comentarios = serializers.serialize('json', comentarios, ensure_ascii=False)
				list_comentarios = simplejson.loads(json_comentarios)
				json_data = simplejson.dumps({'usuario':list_usuario, 'entrada':list_entrada, 'comentarios':list_comentarios} )
				ficheroNohup.write("[**BIE**] Búsqueda de "+request.user.username.encode('utf-8')+" por id de entrada "+ request.GET['texto'].encode('utf-8') +"\n")
				#print "[****] Búsqueda de "+request.user.username.encode('utf-8')+" por id de entrada", request.GET['texto']
			else:
				json_data = simplejson.dumps( {'usuario':"", 'entrada':"", 'comentarios':[]} )
		else:
			json_data = simplejson.dumps( {'alumno':"", 'entrada':"", 'comentarios':[]} )
	ficheroNohup.close()
	return HttpResponse(json_data, mimetype='application/json')



#Valoración de entrada por parte del tutor
def valoraciontutor(request):
	if request.method=='GET':
		idasignatura = request.GET['idasignatura']
		idalumno = request.GET['idalumno']
		identrada = request.GET['identrada']
		valor = request.GET['valor']
		val = Valoracion.objects.get(asignatura=idasignatura,alumno=idalumno)
		val.puntos = val.puntos + int(valor)
		nivel = ActualizarNivel(val.puntos)
		val.nivel = nivel
		val.save()
		entrada = Entrada.objects.get(id=identrada)
		entrada.puntuaciontutor = entrada.puntuaciontutor + int(valor)
		entrada.save()
		
		

#Reseteo de contraseña
def resetear_password(request):
	ficheroNohup = open('nohup.out', 'a')
	encontrado = False
	info = ""
	if request.method=='POST':
		username = request.POST.get('username', '')
		passwd = request.POST.get('password', '')
		usuarios = User.objects.all()
		for usu in usuarios:
			if (usu.username == username):
				encontrado = True
				break;
		if (encontrado == True):
			usuario = User.objects.get(username=username)
			usuario.set_password(passwd)
			usuario.save()
			ficheroNohup.write("[**RC**] Búsqueda de "+request.user.username.encode('utf-8')+" por id de entrada "+ request.GET['texto'].encode('utf-8') +"\n")
			return HttpResponseRedirect(reverse('presentacionprofesor')) 
		else:
			info = "False"
			return render(request, 'planetablogs/resetear_password.html', {'info':info})
	ficheroNohup.close()
	return render(request, 'planetablogs/resetear_password.html', {'info':info})
	
	
	
if __name__ == '__main__':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFG.settings")
	os.environ.setdefault("TIME_ZONE", "Europe/Madrid")
