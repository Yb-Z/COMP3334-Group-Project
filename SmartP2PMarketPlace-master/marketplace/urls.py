"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
import debug_toolbar
from marketapp.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^$', landing),
    # url(r'^register/$', signup),
    # url(r'^login/$',login),
    # url(r'^post/$',feed),
    # url(r'^feed/$',feed_main),
    # url(r'^feed/(?P<username>[\w.@+-]+)$',func),
    # url(r'^like/$',like),
    # url(r'^upvote/',upvote),
    # url(r'^comment/$',comment),
    # url(r'^logout/$', logout),
    path('admin/', admin.site.urls),
    path('', landing),
    path('register/', signup),
    path('login/',login),
    path('post/',feed),
    path('feed/',feed_main),
    path(r'^feed/(?P<username>[\w.@+-]+)$',func),
    path('like/',like),
    path('upvote/',upvote),
    path('comment/',comment),
    path('logout/', logout),
    path('__debug__/', include(debug_toolbar.urls))
]
