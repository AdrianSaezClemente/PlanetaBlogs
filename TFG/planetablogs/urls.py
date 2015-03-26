from django.conf.urls import patterns, include, url
from planetablogs import views

urlpatterns = patterns('',
    # ex: /planetablogs/
    #url(r'^$', views.index, name='index'),
	#url(r'agregar/$', views.nueva_entrada, name='nueva_entrada'),
	#url(r'^ingresar/$',views.ingresar, name='ingresar'),
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
	url(r'^nuevoalumno/$',views.nuevo_alumno, name='nuevo_alumno'),
	url(r'^nuevoprofesor/$',views.nuevo_profesor, name='nuevo_profesor'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/puntuaciones/$',views.puntuaciones, name='puntuaciones'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/infopuntuaciones/$',views.infopuntuaciones, name='infopuntuaciones'),
	url(r'^alumnos/hilo/(?P<idasignatura>\d+)/buscar/$',views.buscar, name='buscar'),
	url(r'^up/$',views.up, name='up'),
	url(r'^down/$',views.down, name='down'),
	url(r'^buscarNickUsuario/$',views.buscarNickUsuario, name='buscarNickUsuario'),
	url(r'^buscarNombreUsuario/$',views.buscarNombreUsuario, name='buscarNombreUsuario'),
	url(r'^buscarIdEntrada/$',views.buscarIdEntrada, name='buscarIdEntrada'),
	url(r'^logout/$', views.salir, name="logout"),
	
    # ex: /PlanetaBlogs/5/
    #url(r'^(?P<preg_id>\d+)/$', views.detail, name='detail'),
    # ex: /PlanetaBlogs/5/results/
    #url(r'^(?P<preg_id>\d+)/results/$', views.results, name='results'),
    # ex: /PlanetaBlogs/5/votar
    #url(r'^(?P<entrada_id>\d+)/votar/$', views.votar, name='votar'),
)

