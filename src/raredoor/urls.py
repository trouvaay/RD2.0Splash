from django.contrib import admin
#admin.autodiscover()

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^', include('landing.urls', namespace='landing')),

    url(r'^accounts/$', TemplateView.as_view(template_name='403.html')),
    url(r'^accounts/signup/$', TemplateView.as_view(template_name='403.html')),
    url(r'^accounts/', include('userena.urls')),

    #url(r'^api/', include('api.urls')),

    url(r'^403/', TemplateView.as_view(template_name='403.html')),
    url(r'^500/', TemplateView.as_view(template_name='500.html')),
)


handler403 = 'raredoor.views.handler403'
handler404 = 'raredoor.views.handler404'
handler500 = 'raredoor.views.handler500'

