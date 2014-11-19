from django.conf.urls import patterns, include, url
from planetablogs import views

urlpatterns = patterns('',
    # ex: /planetablogs/
    url(r'^$', views.index, name='index'),
	#url(r'agregar/$', views.nueva_entrada, name='nueva_entrada'),
	#url(r'^ingresar/$',views.ingresar, name='ingresar'),
	url(r'^nuevousuario/$',views.nuevo_usuario, name='nuevo_usuario'),
	url(r'^puntuaciones/$',views.puntuaciones, name='puntuaciones'),
	url(r'^infopuntuaciones/$',views.infopuntuaciones, name='infopuntuaciones'),
	url(r'^buscar/$',views.buscar, name='buscar'),
	url(r'^up/$',views.up, name='up'),
	url(r'^down/$',views.down, name='down'),
	url(r'^buscarNickUsuario/$',views.buscarNickUsuario, name='buscarNickUsuario'),
	
    # ex: /PlanetaBlogs/5/
    #url(r'^(?P<preg_id>\d+)/$', views.detail, name='detail'),
    # ex: /PlanetaBlogs/5/results/
    #url(r'^(?P<preg_id>\d+)/results/$', views.results, name='results'),
    # ex: /PlanetaBlogs/5/votar
    #url(r'^(?P<entrada_id>\d+)/votar/$', views.votar, name='votar'),
)

