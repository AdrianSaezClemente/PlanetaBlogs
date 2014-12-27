from django.conf.urls import patterns, include, url
from planetablogs import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TFG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^planetablogs/', include('planetablogs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
