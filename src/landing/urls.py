from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

#import views


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='landing/index.html'), name='index'),

)
