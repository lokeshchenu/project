"""CCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin,staticfiles
from home import view
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^contest/(?P<contest>[0-9,a-z,A-Z]+)/$', view.contestLeaderboard),
    url(r'^home/', include('home.urls')),
    url(r'^online/', view.online),
    url(r'^campus/', view.campus),
    url(r'^$',view.index,name='index'),
    url(r'^special/',view.special,name='special'),
    url(r'^logout/$', view.user_logout, name='logout'),
    url(r'^(?P<Id>[0-9,a-z,A-Z]+)/$', view.challenge),
    url(r'^challenge/(?P<contest>[\w\-]+)/(?P<cid>[0-9]+)$', view.challengePage),
    url(r'^challenge/(?P<contest>[0-9,a-z,A-Z]+)/storefile/(?P<user>[0-9,a-z,A-Z]+)/(?P<challenge>[0-9,a-z,A-Z]+)/$',view.storefile),
    url(r'^challenge/(?P<challenge>[0-9,a-z,A-Z]+)/$', view.challengeLeaderboard),

]
