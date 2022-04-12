"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  re_path(r'^blog/', include(blog_urls))
"""
from django.urls import include, re_path
from django.contrib import admin

from marketapp.views import *

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', welcome),
    re_path(r'^register/$', signup),
    re_path(r'^login/$',login),
    re_path(r'^post/$',feed),
    re_path(r'^feed/$',feed_main),
    re_path(r'^feed/(?P<username>[\w.@+-]+)$',func),
    re_path(r'^like/$',like),
    re_path(r'^upvote/',upvote),
    re_path(r'^comment/$',comment),
    re_path(r'^logout/$', logout)
]
