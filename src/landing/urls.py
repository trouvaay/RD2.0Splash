from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^merchant$', views.MerchantView.as_view(), name='merchant'),

    url(r'^accounts/$', TemplateView.as_view(template_name='403.html')),
    url(r'^accounts/', include('userena.urls')),
)
