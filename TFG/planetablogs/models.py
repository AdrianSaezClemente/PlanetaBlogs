from django.db import models  #Para las clases que heredan de models.
from django.contrib.auth.models import User
import sys
	
	
User.add_to_class('imagen', models.ImageField(upload_to='perfiles', verbose_name='Perfil'))
User.add_to_class('estilo', models.CharField(max_length=50))
'''
class Usuario(User):
	docfile = forms.FileField(label='Selecciona un archivo')
	imagen = models.ImageField(upload_to='perfiles', verbose_name='Perfil')
'''

class Profesor(models.Model):
	profesor = models.ForeignKey(User)
	def __unicode__(self):
		return self.profesor.first_name


class Alumno(models.Model):
	alumno = models.ForeignKey(User)
	def __unicode__(self):
		return self.alumno.first_name


class Asignatura(models.Model):
	alumnos = models.ManyToManyField(Alumno, through='Rss')
	profesores = models.ManyToManyField(Profesor)
	titulo = models.CharField(max_length=35)
	descripcion = models.TextField(max_length=150)
	entradas = models.IntegerField()
	creador = models.IntegerField()
	def __unicode__(self):
		return self.titulo
	
	
class Entrada(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.IntegerField()
	titulo = models.CharField(max_length=10)
	fecha = models.DateTimeField()
	descripcion = models.TextField()
	link = models.URLField()
	url_blog = models.URLField()
	totalup = models.IntegerField()
	totaldown = models.IntegerField()
	total = models.IntegerField()
	totalcomentarios = models.IntegerField()
	puntuaciontutor = models.IntegerField()
	visitas = models.IntegerField()
	visitantes = models.CharField(max_length=10000)
	def __unicode__(self):
		return self.titulo


class Extra(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	entrada = models.ForeignKey(Entrada)
	leido = models.CharField(max_length=10000)
	descatado = models.CharField(max_length=10000)
	def __unicode__(self):
		return unicode(self.entrada)
	
	
class Rss(models.Model):
	alumno = models.ForeignKey(Alumno)
	asignatura = models.ForeignKey(Asignatura)
	rss = models.URLField()
	ultima_fecha = models.CharField(max_length=50)
	def __unicode__(self):
		return self.rss
	
	
class Diseno(models.Model):
	usuario = models.ForeignKey(User)
	estilo = models.CharField(max_length=35)
	imagen = models.ImageField(upload_to='disenos', verbose_name='Disenos')
	def __unicode__(self):
		return self.rss
	

class Valoracion(models.Model):
	alumno = models.ForeignKey(Alumno)
	asignatura = models.ForeignKey(Asignatura)
	puntos = models.IntegerField()
	nivel = models.IntegerField()
	def __unicode__(self):
		return unicode(self.alumno)
	

class Up(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	def __unicode__(self):
		return self.entrada
	
	
class Down(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	def __unicode__(self):
		return self.entrada
	
	
class Comentario(models.Model):
	asignatura = models.ForeignKey(Asignatura)
	alumno = models.ForeignKey(Alumno)
	entrada = models.ForeignKey(Entrada)
	fecha = models.DateTimeField()
	descripcion = models.TextField()
	username = models.CharField(max_length=35)
	def __unicode__(self):
		return unicode(self.alumno)
	
	