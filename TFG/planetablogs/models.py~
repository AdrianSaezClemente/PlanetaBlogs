from django.db import models  #Para las clases que heredan de models.
import sys

class Usuario(models.Model):
	nick = models.CharField(max_length=40)
	nombre_apellidos = models.CharField(max_length=40)	
	rss = models.URLField()
	password = models.CharField(max_length=40)
	entradas = models.IntegerField()
	url_blog = models.URLField()
	#email = models.EmailField(max_length=70)
	def __unicode__(self):
		return self.nombre_apellidos

class Entrada(models.Model):
	usuario = models.ForeignKey(Usuario)
	titulo = models.CharField(max_length=80)
	link = models.URLField()
	fecha = models.CharField(max_length=40)
	descripcion = models.TextField()
	def __unicode__(self):
		return self.usuario.nombre_apellidos
