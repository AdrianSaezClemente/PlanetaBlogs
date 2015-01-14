from django.db import models  #Para las clases que heredan de models.
from django.contrib.auth.models import User
import sys
	
	
class Profesor(models.Model):
	profesor = models.ForeignKey(User)
	def __unicode__(self):
		return self.profesor.first_name


class Alumno(models.Model):
	alumno = models.ForeignKey(User)
	def __unicode__(self):
		return self.alumno.first_name


class Entrada(models.Model):
	alumno = models.ForeignKey(Alumno)
	titulo = models.CharField(max_length=80)
	link = models.URLField()
	fecha = models.CharField(max_length=40)
	descripcion = models.TextField()
	def __unicode__(self):
		return self.alumno


class Asignatura(models.Model):
	alumnos = models.ManyToManyField(Alumno)
	profesores = models.ManyToManyField(Profesor)
	titulo = models.CharField(max_length=80)
	descripcion = models.TextField()
	#rss = models.URLField()
	#puntuaciontotal = models.IntegerField()
	#nivel = models.IntegerField()
	def __unicode__(self):
		return self.titulo


class Valoracion(models.Model):
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	up = models.IntegerField()
	down = models.IntegerField()
	def __unicode__(self):
		return self.alumno
	

class Comentario(models.Model):
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	fecha = models.CharField(max_length=40)
	descripcion = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.alumno
	
	