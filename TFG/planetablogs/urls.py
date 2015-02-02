from django.conf.urls import patterns, include, url
from planetablogs import views

urlpatterns = patterns('',
    # ex: /planetablogs/
    url(r'^$', views.index, name='index'),
	#url(r'agregar/$', views.nueva_entrada, name='nueva_entrada'),
	#url(r'^ingresar/$',views.ingresar, name='ingresar'),
	url(r'^login/$', views.inicio, name='login'),
	url(r'^presentacion_profesor/$', views.presentacionprofesor, name='presentacionprofesor'),
	url(r'^presentacion_alumno/$', views.presentacionalumno, name='presentacionalumno'),
	url(r'^agregarasignaturaprofesor/$', views.agregarasignaturaprofesor, name='agregarasignaturaprofesor'),
	url(r'^eliminarasignaturaprofesor/$', views.eliminarasignaturaprofesor, name='eliminarasignaturaprofesor'),
	url(r'^eliminarasignaturaalumno/$', views.eliminarasignaturaalumno, name='eliminarasignaturaalumno'),
	#url(r'^agregarasignaturaprofesor/$', 'redirect_to', {'url': '/planetablogs/presentacion_profesor/'}),
	url(r'^nuevoalumno/$',views.nuevo_alumno, name='nuevo_alumno'),
	url(r'^nuevoprofesor/$',views.nuevo_profesor, name='nuevo_profesor'),
	url(r'^puntuaciones/$',views.puntuaciones, name='puntuaciones'),
	url(r'^infopuntuaciones/$',views.infopuntuaciones, name='infopuntuaciones'),
	url(r'^buscar/$',views.buscar, name='buscar'),
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

