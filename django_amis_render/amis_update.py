# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.http import HttpResponse



"""
{"pages":[{"id":"1","icon":"fa fa-file","path":"hello-world","label":"Hello world","schema":{"type":"page","title":"Hello world","body":"初始页面"}}],"theme":"default","asideFixed":true,"asideFolded":false,"offScreen":false,"addPageIsOpen":false,"preview":false,"isMobile":false}
"""
from .models import AmisRenderList
import os
from django.conf import settings
import json


def update_amis_local_to_editor_one_file(route_id):
    base_dir = settings.BASE_DIR

    if settings.DEFAULT_AMIS_JSON_DIR is not None:
        #return HttpResponse('需要设置json本地文件目录', status=400)
        json_dir = settings.DEFAULT_AMIS_JSON_DIR
    else:
        json_dir = 'static/django_amis_render/json'

    pages=[]
    all_dir = os.path.join(base_dir, json_dir)

    ajf = AmisRenderList.objects.get(id=route_id)
    file_full_path=os.path.join(all_dir, ajf.file_path)
    if os.path.isfile(file_full_path):
        f = open(file_full_path, 'r', encoding='utf-8')
        data = f.read()
        f.close()
    else:
        #file not exist
        data = "{}"
    pages.append({'icon': '', 'id': str(1), 'label': ajf.file_name, 'path': ajf.file_name.replace('.json', ''), 'schema': json.loads(data)})

    store_data = {'pages':pages}
    store_data['addPageIsOpen']=False
    store_data['asideFixed'] = True
    store_data['isMobile'] = False
    store_data['offScreen'] = False
    store_data['theme'] = 'default'
    store_data['asideFolded'] = False


    return HttpResponse(json.dumps({'data':store_data,   }), status=200)

def update_amis_local_to_editor(request):
    route_id = request.POST.get('route_id')

    if route_id is not None:
        return update_amis_local_to_editor_one_file(route_id)

    return HttpResponse(json.dumps({'data':'ok',   }), status=200)

def update_amis_editor_to_local(request):

    if settings.DEFAULT_AMIS_JSON_DIR is not None:
        #return HttpResponse('需要设置json本地文件目录', status=400)
        json_dir = settings.DEFAULT_AMIS_JSON_DIR
    else:
        json_dir = 'static/django_amis_render/json'


    base_dir = settings.BASE_DIR
    all_dir = os.path.join(base_dir, json_dir)


    store = request.POST.get('store')
    print(store)
    #store=store.encode('utf-8').decode('raw_unicode_escape') #.decode('unicode_escape')

    pages = json.loads(store)
    pages=pages['pages']
    for i in pages:
        file_name = i['label']
        full_file_name = os.path.join(all_dir, file_name)
        print('saving file:', full_file_name)
        f = open(full_file_name, 'w', encoding='utf-8')
        f.write(json.dumps(i['schema'], ensure_ascii=False))#.encode('utf-8')
        f.close()

    return HttpResponse('ok', status=200)

