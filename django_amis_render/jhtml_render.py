__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os
from django.http import HttpResponse

from .models import AmisRenderList
from django.conf import settings
import platform
from django.urls import get_urlconf
from django.shortcuts import render

g_sys_name = platform.system()


def no_route_found(request):
    nof = HttpResponse()
    nof.content = 'no page found:'+request.path
    nof.status_code = 404
    url_confs = get_urlconf()
    print(url_confs)

    return nof

def load_default_file(request):
    return no_route_found(request)


def render_this_one(request, re_one):

    file_url = re_one.json_file_url
    page_name = re_one.html_template
    print('render_amis_json', file_url)
    if (page_name is not None) and len(page_name) > 0:
        page_name = settings.BASE_DIR + page_name
    else:
        page_name = 'html/index_for_json.html'
    if len(file_url)>3:
        if file_url[-4:]=='html':
            page_name = file_url
    return render(request, page_name, {'json_to_render_file_url': file_url})


def jhtml_render(request):
    from django.urls import reverse
    path = request.path
    print(path)

    re_all = AmisRenderList.objects.all()
    for i in re_all:
        try:
            link_to = reverse(i.url_name)
        except Exception as e:
            link_to = None

        if i.page_url_all != link_to:
            i.page_url_all = link_to
            i.save()

    for i in re_all:
        if i.page_url_all is None:
            print('jhtml-render: one will not show as no url found id=',i.id)
            continue
        if i.page_url_all.strip() == path.strip():
            return render_this_one(request, i)

    #其他文件
    return load_default_file(request)