__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os

import platform

from django.http import JsonResponse
from django.shortcuts import render

g_sys_name = platform.system()


def no_route_found(request):
    from django.http import HttpResponse
    from django.urls import get_urlconf

    nof = HttpResponse()
    nof.content = 'no page found:'+request.path
    nof.status_code = 404
    url_confs = get_urlconf()
    print(url_confs)

    return nof

def load_default_file(request):
    return no_route_found(request)


def render_this_one(request, re_one):
    from django.conf import settings
    from django.shortcuts import render

    if re_one.file_type=='json':
        #static amis json file render
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
    else:#if re_one.file_type=='temp_json':
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




def render_template_json(request):
    """
    函数用于渲染模板的amis json文件
    """
    from django.urls import reverse
    from .models import AmisRenderList

    path = request.path
    print(path)

    re_all = AmisRenderList.objects.all()

    for i in re_all:
        if i.json_file_url is None:
            continue
        if i.json_file_url.strip() == path.strip():
            file_path = i.file_path.replace('\\','/')
            pos = file_path.find('templates/')
            pos += 10
            file_path = i.file_path[pos:]
            if i.json_render_dict is None:
                return render(request, file_path)
            else:
                return render(request, file_path, context=eval(i.json_render_dict))

    return JsonResponse({'nothing':'nothing'})


def update_page_url_all():
    from django.urls import reverse
    from .models import AmisRenderList
    re_all = AmisRenderList.objects.all()
    for i in re_all:
        try:
            link_to = reverse(re_all[0].app_name+':'+i.url_name)
        except Exception as e:
            link_to = None

        if i.file_type == 'temp_json':
            try:
                link_to2 = reverse(re_all[0].app_name + ':' + i.url_name+'_tjson')
            except Exception as e:
                link_to2 = None

            if i.json_file_url != link_to2:
                i.json_file_url = link_to2
                i.save()

        if i.page_url_all != link_to:
            i.page_url_all = link_to
            i.save()

    return re_all

def jhtml_render(request):
    re_all = update_page_url_all()

    path = request.path
    print(path)

    for i in re_all:
        if i.page_url_all is None:
            print('jhtml-render: one will not show as no url found id=',i.id)
            continue
        if i.page_url_all.strip() == path.strip():
            return render_this_one(request, i)

    #其他文件
    return load_default_file(request)