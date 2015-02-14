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
	fecha = models.DateTimeField()
	descripcion = models.TextField()
	#numero_comentarios = models.IntegerField()
	def __unicode__(self):
		return self.titulo


class Asignatura(models.Model):
	alumnos = models.ManyToManyField(Alumno, through='Rss')
	profesores = models.ManyToManyField(Profesor)
	titulo = models.CharField(max_length=50)
	descripcion = models.TextField(max_length=150)
	def __unicode__(self):
		return self.titulo


class Rss(models.Model):
	alumno = models.ForeignKey(Alumno)
	asignatura = models.ForeignKey(Asignatura)
	rss = models.URLField()
	ultima_fecha = models.DateTimeField(auto_now_add=True)
	url_blog = models.URLField()
	def __unicode__(self):
		return self.rss
	

class Valoracion(models.Model):
	alumno = models.ForeignKey(Alumno)
	asignatura = models.ForeignKey(Asignatura)
	puntos = models.IntegerField()
	def __unicode__(self):
		return self.alumno
	

class Up(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	total = models.IntegerField()
	def __unicode__(self):
		return self.total
	
	
class Down(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	total = models.IntegerField()
	def __unicode__(self):
		return self.total
	
	
class Comentario(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	fecha = models.DateTimeField()
	descripcion = models.TextField()
	def __unicode__(self):
		return self.alumno
	
	