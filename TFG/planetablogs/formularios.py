from planetablogs.models import Entrada, Usuario
from django import forms
from django.forms import ModelForm
from django.utils import timezone  
from django.core.exceptions import ValidationError
from datetime import datetime


class FormularioRegistro(ModelForm):
	class Meta:
		model = Usuario
		exclude = ('entradas','url_blog','puntuaciontotal','nivel')

class FormularioIdentidad(ModelForm):
	class Meta:
		model = Usuario
		exclude = ('nombre_apellidos','rss','entradas','url_blog',)
