
from django.conf.urls import include,url
from django.contrib import admin

import CCMS
from home import view

app_name='home'

urlpatterns = [
    url(r'^register/$',view.register,name='register'),
    url(r'^user_login/$',view.user_login,name='user_login'),
    url(r'^(?P<CampusContest_id>[0-9,a-z,A-Z]+)/$', view.campus_contest),

]