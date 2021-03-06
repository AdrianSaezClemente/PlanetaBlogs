from django.conf.urls import patterns, include, url
from planetablogs import views
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles import views

urlpatterns = patterns('',
	url(r'^login/$', views.inicio, name='login'),
	url(r'^tutores/$', views.presentacionprofesor, name='presentacionprofesor'),
	url(r'^alumnos/$', views.presentacionalumno, name='presentacionalumno'),
	url(r'^agregarasignaturaprofesor/$', views.agregarasignaturaprofesor, name='agregarasignaturaprofesor'),
	url(r'^eliminarasignaturaprofesor/$', views.eliminarasignaturaprofesor, name='eliminarasignaturaprofesor'),
	url(r'^eliminarasignaturaalumno/$', views.eliminarasignaturaalumno, name='eliminarasignaturaalumno'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/$', views.mostrarhiloalumno, name='mostrarhiloalumno'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/$', views.mostrarhiloprofesor, name='mostrarhiloprofesor'),
	url(r'^eliminarcomentario/$', views.eliminarcomentario, name='eliminarcomentario'),
	url(r'^agregarcomentario/$', views.agregarcomentario, name='agregarcomentario'),
	url(r'^eliminarentrada/$', views.eliminarentrada, name='eliminarentrada'),
	url(r'^eliminaralumno/$', views.eliminaralumno, name='eliminaralumno'),
	url(r'^valoraciontutor/$', views.valoraciontutor, name='valoraciontutor'),
	url(r'^nuevoalumno/$',views.nuevo_alumno, name='nuevo_alumno'),
	url(r'^nuevoprofesor/$',views.nuevo_profesor, name='nuevo_profesor'),
	url(r'^cambiarestilo/$',views.cambiarestilo, name='cambiarestilo'),
	url(r'^eliminardiseno/$',views.eliminardiseno, name='eliminardiseno'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/puntuaciones/$',views.puntuaciones, name='puntuaciones'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/estadisticas/$',views.estadisticas, name='estadisticas'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/infopuntuaciones/$',views.infopuntuaciones, name='infopuntuaciones'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/buscar/$',views.buscar, name='buscar'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/ayuda/$',views.ayuda, name='ayuda'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/puntuaciones/$',views.puntuaciones_tutor, name='puntuaciones_tutor'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/estadisticas/$',views.estadisticas_tutor, name='estadisticas_tutor'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/infopuntuaciones/$',views.infopuntuaciones_tutor, name='infopuntuaciones_tutor'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/buscar/$',views.buscar_tutor, name='buscar_tutor'),
	url(r'^tutores/hilo/(?P<idasignatura>\d+)/ayuda/$',views.ayuda_tutor, name='ayuda_tutor'),
	url(r'^up/$',views.up, name='up'),
	url(r'^down/$',views.down, name='down'),
	url(r'^buscarNickUsuario/$',views.buscarNickUsuario, name='buscarNickUsuario'),
	url(r'^buscarNombreUsuario/$',views.buscarNombreUsuario, name='buscarNombreUsuario'),
	url(r'^buscarIdEntrada/$',views.buscarIdEntrada, name='buscarIdEntrada'),
	url(r'^entradaleida/$',views.entradaleida, name='entradaleida'),
	url(r'^entradaleidatutor/$',views.entradaleidatutor, name='entradaleidatutor'),
	url(r'^mostrarvisitasusuarios/$',views.mostrarvisitasusuarios, name='mostrarvisitasusuarios'),
	url(r'^logout/$', views.salir, name="logout"),
	url(r'^tutores/resetear_password/$', views.resetear_password, name="resetear_password"),
	url(r'^agregardisenoalumno/$', views.agregardisenoalumno, name='agregardisenoalumno'),
)
'''
if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
	urlpatterns += patterns('',
			url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)
'''