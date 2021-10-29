# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.db.models import Q
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from .models import RouteExec
from django.shortcuts import render
from AmisBack.models import RouteExec, AmisJsonFile, AmisCfg
from .my_rest_api import my_rest_viewsetB
from .update_models import parse_params

s_custom_init_rest = 0

from django.urls import get_urlconf

def no_route_found(request):
    from amis_django.urls import urlpatterns
    nof = HttpResponse()
    nof.content = 'no page found:'+request.path
    nof.status_code = 404
    url_confs = get_urlconf()
    print(url_confs)

    return nof

def render_amis_json(request, amis_json):
    json_file_name = amis_json.file_name
    file_url = '/json/'+json_file_name
    page_name = amis_json.render_html
    print('render_amis_json', file_url)
    if (page_name is None) or len(page_name) == 0:
        page_name = 'html/index_for_json.html'
    return render(request, page_name, {'json_to_render_file_url': file_url, 'module_name': request.path})

def render_this_one(request, re_one):
    if re_one.re_type == 'py':
        pass  # python
    elif re_one.re_type == 'sql':
        pass  # sql
    elif re_one.re_type == 'json':
        pass  # json file
        return render(request, 'json/' + re_one.page_name)
    else:
        # unknown type
        nof = HttpResponse()
        nof.content = 'unknown type:' + str(re_one.re_type)
        nof.status_code = 400
        return nof


import os

from django.conf import settings
import platform
g_sys_name = platform.system()
#Windows Linux
def load_default_file(request):
    BASE_DIR = settings.BASE_DIR
    path = request.path
    global g_sys_name
    print(path)
    if path=='/':
        #no root index page
        return no_route_found(request)

    if len(path)<2:
        return no_route_found(request)

    base_dir = str(BASE_DIR)
    #path = path.replace('/custom/', '')
    path = path[1:]
    path_all = os.path.join(os.path.join(base_dir , settings.DEFAULT_AMIS_FILE_DIR), path)
    if g_sys_name=='Windows':
        path_all = path_all.replace('/', '\\')
    print('load_default_file', path_all)

    if os.path.isfile(path_all):
        return render(request, path)

    return no_route_found(request)


def my_custom_view(request):
    path = request.path
    print(path)

    re_all = RouteExec.objects.all()
    for i in re_all:
        if i.route.strip() == path.strip():
            return render_this_one(request, i)

    # 渲染json文件
    for i in AmisJsonFile.objects.all():
        if i.route.strip() == path.strip():
            return render_amis_json(request, i)

    #其他文件
    return load_default_file(request)


def upate_route(request):
    return HttpResponse("ok")


# 所选题目
# choice_problems = my_rest_viewsetB(Problem, 'PromblemSetV', ['id', 'name_english', 'name', 'is_used'], filter_fields=('is_used',))


if __name__ == '__main__':
    pass
