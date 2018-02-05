# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from libs import (
    create_captcha_img, get_mobile_code_libs,regist,auth_captche,login
)

# Create your views here.

def captcha(request):
    """01生成图形验证码函数"""
    getdate = request.GET.copy()
    pre_code = getdate.get('pre_code', '')
    code = getdate.get('code', '')
    img_data = create_captcha_img(pre_code, code)
    response = HttpResponse(img_data, content_type='image/jpg')
    return response

def send_mobile_code(request):
    """02发送手机短信验证码函数"""
    if request.method == "POST":
        postdata = request.POST.copy()
        mobile = postdata.get('mobile', '')
        code = postdata.get('code', '')
        captcha = postdata.get('captcha', '')

        result = get_mobile_code_libs(mobile, code, captcha)
        if result['status'] is True: #id(aa) == id(None)
            return JsonResponse({'status': 200, 'msg': result['msg']})
        else:
            return JsonResponse({'status': 400, 'msg': result['msg']})

def user_regist(request):
    """03用户注册函数"""
    if request.method == "POST":
        postdata = request.POST.copy()
        mobile = postdata.get('mobile', '')
        name = postdata.get('name', '')
        mobile_captcha = postdata.get('mobile_captcha', '')
        code = postdata.get('code', '')
        captcha = postdata.get('captcha', '')
        password1 = postdata.get('password1', '')
        password2 = postdata.get('password2', '')

        result = regist(request, mobile, name, mobile_captcha, code,
                        captcha, password1, password2)
        if result['status'] is False:
            kw = {'message': result['msg']}
            return render(request,  'account/auth_regist.html', kw)
        else:
            return redirect('/account/user_login/')
    return render(request, 'account/auth_regist.html')


def user_login(request):
    if request.method == "POST":
        postdata = request.POST.copy()
        name = postdata.get('name', '')
        password = postdata.get('password', '')
        code = postdata.get('code', '')
        captcha_code = postdata.get('captcha', '')
        remember = postdata.get('remember', '')

        result = auth_captche(captcha_code, code)
        if result['status'] is False:
            return JsonResponse({'status': 400, 'msg': result['msg']})

        result = login(request, name, password, remember)
        if result['status'] is False:
            return JsonResponse({'status': 400, 'msg': result['msg']})
        else:
            if result['user'].loginnum == 1:
                return JsonResponse({'status': 200, 'msg': '你好新用户'})
            else:
                return JsonResponse({'status': 200, 'msg': result['msg']})

    return render(request, 'account/auth_login.html')