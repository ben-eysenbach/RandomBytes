from django.conf.urls import patterns, include, url
from poll_graph.views import graph, about

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('about', about),
    ('(?!about)', graph),
)
