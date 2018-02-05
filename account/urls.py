#coding=utf-8
from django.conf.urls import url, include
from views import (
    user_regist, captcha,send_mobile_code, user_login
)

urlpatterns = [
    url(r'^user_regist/$', user_regist, name='user_regist'),
    url(r'^user_login/$', user_login, name='user_login'),
    url(r'^captcha/$', captcha, name='captcha'),
    url(r'^send_mobile_code/$', send_mobile_code, name='send_mobile_code'),
]