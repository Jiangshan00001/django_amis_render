__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os

import platform

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django_amis_render.get_url_from_name import get_url_from_name


g_sys_name = platform.system()


def render_template_json(request, file_path, json_render_dict=None, json_render_func=None):
    """
    函数用于渲染模板的amis json文件
    """
    from django.urls import reverse
    if file_path is None:
        return JsonResponse({'nothing': 'nothing'})

    file_path = file_path.replace('\\','/')
    pos = file_path.find('templates/')
    pos += 10
    file_path = file_path[pos:]

    if json_render_dict=='':
        json_render_dict=None
    if json_render_dict is None:
        json_render_dict = {}

    if json_render_func =='':
        json_render_func=None
    if json_render_func is not None:
        json_render_dict.update(json_render_func(request, json_render_dict))

    print('render_template_json:',file_path)
    return render(request, file_path, context=json_render_dict)

def jhtml_render(request, file_type=None,json_file_url=None, html_template=None, json_render_dict=None, json_render_func=None, file_path=None, url_name=None, app_name=None):
    """

    :param request:
    :param file_type: json/temp_json
    :param json_file_url:
    :param html_template:模板文件路径，不包含templates
    :param render_var_dict_str: 渲染变量dict
    :return:
    """
    path = request.path
    print(path)
    from django.conf import settings
    from django.shortcuts import render

    if file_type=='temp_json':
        is_got, json_file_url = get_url_from_name(url_name+'_tjson', app_name)
        if not is_got:
            print('ERROR: no json file url found:',url_name, app_name, file_path)


    render_dict = {'json_to_render_file_url': json_file_url}
    if json_render_dict is not None:
        render_dict.update(json_render_dict)
    if json_render_func is not None:
        render_dict.update(json_render_func(request, json_render_dict))
    page_name = html_template
    if (page_name is not None) and len(page_name) > 0:
        page_name = page_name  # settings.BASE_DIR /
    else:
        page_name = 'html/index_for_json.html'
    if len(json_file_url) > 3:
        if json_file_url[-4:] == 'html':
            page_name = json_file_url

        #static amis json file render
        ##if re_one.file_type=='temp_json':
    return render(request, page_name, render_dict)


##################################
#render不再依赖于数据库，这样才能保证生成的app不需要依赖数据库中的数据就可以直接运行













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




def render_template_json_old(request):
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
            app_url_name = re_all[0].app_name+':'+i.url_name
            link_to = reverse(i.url_name, current_app=re_all[0].app_name)
        except Exception as e:
            link_to = None
            print('no route found:',app_url_name)
        if i.file_type == 'temp_json':
            try:
                app_url_name = re_all[0].app_name + ':' + i.url_name+'_tjson'
                link_to2 = reverse(i.url_name+'_tjson', current_app=re_all[0].app_name)
            except Exception as e:
                link_to2 = None
                print('no route found:',app_url_name)

            if i.json_file_url != link_to2:
                i.json_file_url = link_to2
                i.save()

        if i.page_url_all != link_to:
            i.page_url_all = link_to
            i.save()

    return re_all





def jhtml_render_old(request):
    re_all = update_page_url_all()

    path = request.path
    print(path)

    for i in re_all:
        if i.page_url_all is None:
            continue
        if i.page_url_all.strip() == path.strip():
            return render_this_one(request, i)

    #其他文件
    return load_default_file(request)