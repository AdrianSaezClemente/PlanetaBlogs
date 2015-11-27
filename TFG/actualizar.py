#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFG.settings")
os.environ.setdefault("TIME_ZONE", "Europe/Madrid")
import sys
from django.conf import settings
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from planetablogs.models import Entrada, Alumno, Profesor, Asignatura, Rss, Valoracion, Comentario, Up, Down
from planetablogs.formularios import FormularioRegistro, FormularioIdentidad
from django.template import RequestContext
import feedparser
from time import mktime
from datetime import datetime, timedelta
from dateutil import tz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import time
import re


#Obtiene el RSS con feedparser
def ObtenerRss(url):
	rss = feedparser.parse(url)
	return rss
	


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


	
#Guardar 8 puntos de valoracion para el alumno que guarda la entrada
def GuardarValoracionEntrada(idasignatura,idalumno):
	val = Valoracion.objects.filter(asignatura_id=idasignatura).get(alumno_id=idalumno)
	val.puntos = val.puntos + 8
	nivel = ActualizarNivel(val.puntos)
	val.nivel = nivel
	val.save()
	
	
	
#Guardar la entrada con un identificador dentro de cada asignatura
def ConseguirNumeroEntradaEnAsignatura(asignatura):
	asignatura.entradas = asignatura.entradas + 1
	entrada = asignatura.entradas
	asignatura.save()
	return entrada
	
	
	
def ConvertirDescripcionSinTags(html):
	text = html

	special = {
		'&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
		'&lt;'   : '<', '&gt;'  : '>'
	}
	for (k,v) in special.items():
		text = text.replace (k, v)
		
	text = re.sub('<p><br /></p>', '</br>', text)
	text = re.sub('<br /><br /><br />', '</br>', text)
	text = re.sub('<br /><br />', '</br>', text)
	text = re.sub('<br />', '</br>', text)
	text = re.sub('<br>', '</br>', text)
	text = re.sub('<b>', '<strong>', text)
	text = re.sub('</b>', '</strong>', text)
	text = re.sub('</strong></br>', '</strong>', text)
	text = re.sub('<h2>', '<h4>', text)
	text = re.sub('</h2>', '</h4>', text)
	text = re.sub('<h3>', '<h4>', text)
	text = re.sub('</h3>', '</h4>', text)
	#text = re.sub('<p>', '', text)
	#text = re.sub('</p>', '</br>', text)
	#text = re.sub('<img', '<p><img', text)
	text = re.sub(' /></p>', ' /></p></br>', text)
	#text = re.sub('<iframe', '<p><iframe', text)
	text = re.sub('/iframe>', '/iframe></p></br>', text)
	#text = re.sub('[</br>]+', '</br>', text)

	#text = re.sub('<[^>]*>', '', text)
	return text


#Parsear las etiquetas del RSS y devuelve una entrada
def ParsearEtiquetasRss(objetorss,i):
	from_zone = tz.tzutc()				#Coge zona UTC
	rss = ObtenerRss(objetorss.rss)
	idalumno = objetorss.alumno_id
	alumno = Alumno.objects.get(id=idalumno)
	idasignatura = objetorss.asignatura_id
	asignatura = Asignatura.objects.get(id=idasignatura)
	entrada = ConseguirNumeroEntradaEnAsignatura(asignatura)
	titulo = rss.entries[i].title
	link = rss.entries[i].link
	url_blog = rss.feed.link
	pubDate = rss.entries[i].published_parsed
	fecha_entrada = datetime.fromtimestamp(mktime(pubDate))	+ timedelta(hours=1)	#Convertir fecha parseada a DateTime (Una hora más por desfase horario)
	utc = fecha_entrada.replace(tzinfo=from_zone) 									#Convierte fecha DateTime a zona UTC
	fecha = utc.strftime("%Y-%m-%d %H:%M:%S")										#fecha se guarda en un objeto Entrada con dos horas menos de la hora local.
	descripcion_tags = rss.entries[i].description
	descripcion = ConvertirDescripcionSinTags(descripcion_tags)
	entrada = Entrada(asignatura=asignatura,alumno=alumno,entrada=entrada,titulo=titulo,fecha=fecha,descripcion=descripcion,link=link,url_blog=url_blog,totalup=0,totaldown=0,total=0,totalcomentarios=0)
	entrada.save()
	GuardarValoracionEntrada(idasignatura,idalumno)



#Devuelve una entrada
def ParsearEntrada(objetorss,i):
	entrada = ParsearEtiquetasRss(objetorss,i)



#Guarda la entrada en la bbdd
def GuardarEntrada(objetorss,i):
	ParsearEntrada(objetorss,i)



#Actualiza usuarios
def ActualizarUsuarios():
	from_zone = tz.tzutc()				#Coge zona UTC
	lista_rss = Rss.objects.all()
	for objetorss in lista_rss:
		rss = ObtenerRss(objetorss.rss)
		lon = len(rss.entries)
		if lon == 0:
			pass
		else:
			for i in range(lon,0,-1):
				pubDate = rss.entries[i-1].published_parsed 			
				fecha_entrada = datetime.fromtimestamp(mktime(pubDate))	+ timedelta(hours=1)	#Convertir fecha parseada a DateTime (Una hora más por desfase horario)
				utc = fecha_entrada.replace(tzinfo=from_zone) 									#Convierte fecha DateTime a zona UTC
				fecha_entrada_str = utc.strftime("%Y-%m-%d %H:%M:%S")							#fecha_entrada_str tiene mismo formato que ultima_entrada_str
				print "Entrada nueva: "+fecha_entrada_str
				ultima_entrada_str = objetorss.ultima_fecha
				print "Ultima entrada: "+ultima_entrada_str
				if (fecha_entrada_str > ultima_entrada_str):			#fecha entrada nueva > fecha ultima entrada => Se guarda la entrada
					GuardarEntrada(objetorss,i-1)
					objetorss.ultima_fecha = fecha_entrada_str
					print "Guardada: "+fecha_entrada_str
					objetorss.save()
	return lista_rss



if __name__ == '__main__':
	elements = ['iframe', 'embed', 'object',]
	elements += list(feedparser._HTMLSanitizer.acceptable_elements)
	feedparser._HTMLSanitizer.acceptable_elements = set(elements)
	ActualizarUsuarios()
    
    
    