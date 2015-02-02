from planetablogs.models import Entrada, Alumno, Profesor, Asignatura, Rss
from django import forms
from django.forms import ModelForm
from django.utils import timezone  
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User

'''
class FormularioRegistro(ModelForm):
	class Meta:
		model = Usuario
		exclude = ('entradas','url_blog','puntuaciontotal','nivel')
'''
class FormularioIdentidad(ModelForm):
	class Meta:
		model = Alumno
		exclude = ('nombre_apellidos','rss','entradas','url_blog',)


class FormularioRegistro(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        #exclude = ('rss',)
        widgets = {
            'password': forms.PasswordInput(),
        }
		

class FormularioHilo(ModelForm):
	class Meta:
		model = Asignatura
		fields = ['titulo', 'descripcion']
		
		
class FormularioAgregarHilo(ModelForm):
	class Meta:
		model = Asignatura
		fields = ['titulo']
		

class FormularioAgregarRSS(ModelForm):
	class Meta:
		model = Rss
		fields = ['rss','asignatura']