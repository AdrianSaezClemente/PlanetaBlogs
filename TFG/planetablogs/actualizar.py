#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from planetablogs.models import Entrada, Alumno, Profesor, Asignatura
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
		url_blog = rss.feed.link
		if (usuario.url_blog=='') & (usuario.entradas==0):	#Usuario se acaba de registrar
			usuario.url_blog = url_blog						#Guardar url del blog
			usuario.entradas = lon							#y un contador de entradas del blog
			usuario.save()
			GuardarEntradas(usuario,lon)
			actualizacion = actualizacion + 1
		else:
			actualizacion = ComprobarEntradas(usuario,lon,actualizacion)		
	if actualizacion>0:
		print "Actualizaciones: "+str(actualizacion)
		lista_usuarios = Usuario.objects.all()
		return lista_usuarios
	else:
		print "No ha habido actualizaciones: "+str(actualizacion)
		return lista_usuarios

if __name__ == '__main__':
	ActualizarUsuarios()
    
    
    