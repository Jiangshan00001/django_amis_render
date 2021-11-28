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
from pathlib import Path


def get_amis_json_file_path(route_id):
    data_all = AmisRenderList.objects.filter(id=route_id).all()
    if len(data_all) == 0:
        return None

    ajf = data_all[0]
    base_dir = settings.BASE_DIR

    file_full_path= os.path.join(base_dir, ajf.file_path)
    if os.path.isfile(file_full_path):
        return file_full_path

    return None


def get_amis_json_file_content(file_full_path):
    """

    :param file_full_path:
    :return: 字符串，文件内容
    """
    if os.path.isfile(file_full_path):
        f = open(file_full_path, 'r', encoding='utf-8-sig')
        data = f.read()
        f.close()
        return data
    return None

def save_amis_json_file_content(file_full_path, content):
    """

    :param file_full_path:
    :param content: dict
    :return:
    """
    if os.path.isfile(file_full_path):
        print('saving file:', file_full_path)
        f = open(file_full_path, 'w', encoding='utf-8-sig')
        f.write(json.dumps(content, ensure_ascii=False))  # .encode('utf-8')
        f.close()
        return 1
    return 0


def update_amis_local_to_editor_one_file(route_id):
    file_full_path=get_amis_json_file_path(route_id)
    data = get_amis_json_file_content(file_full_path)
    if data is None:
        data={}

    pages = []
    file_name = Path(file_full_path)
    pages.append({'icon': '', 'id': str(route_id), 'label': file_name.stem,
                  'path': file_name.stem, 'schema': json.loads(data)})

    store_data = {'pages':pages}
    store_data['addPageIsOpen']=False
    store_data['asideFixed'] = True
    store_data['isMobile'] = False
    store_data['offScreen'] = False
    store_data['theme'] = 'default'
    store_data['asideFolded'] = False


    return HttpResponse(json.dumps({'data':store_data,   }), status=200)

    # data_all = AmisRenderList.objects.filter(id=route_id).all()
    # if len(data_all)==0:
    #     return 1
    #
    # base_dir = settings.BASE_DIR
    # print('update_amis_local_to_editor_one_file', base_dir)
    # #base_dir = Path(base_dir)
    #
    # ajf = data_all[0]
    # print('ajf.file_path', ajf.file_path)
    # if len(ajf.file_path)>0 and ajf.file_path[0]=='\\':
    #     ajf.file_path=ajf.file_path[1:]
    #
    # file_full_path= os.path.join(base_dir, ajf.file_path)
    # if os.path.isfile(file_full_path):
    #     f = open(file_full_path, 'r', encoding='utf-8-sig')
    #     data = f.read()
    #     f.close()
    # else:
    #     print('file not exist:', file_full_path)
    #     #file not exist
    #     data = "{}"


def update_amis_local_to_editor(request):
    route_id = request.POST.get('route_id')

    if route_id is not None:
        return update_amis_local_to_editor_one_file(route_id)

    return HttpResponse(json.dumps({'data':'ok',   }), status=200)

def update_amis_editor_to_local(request):


    base_dir = settings.BASE_DIR

    store = request.POST.get('store')
    print(store)
    #store=store.encode('utf-8').decode('raw_unicode_escape') #.decode('unicode_escape')

    pages = json.loads(store)
    pages=pages['pages']
    for i in pages:
        file_name = i['label']
        id = i['id']
        full_file_name = get_amis_json_file_path(id)

        # arl = AmisRenderList.objects.filter(id=id).all()
        # if len(arl)==0:
        #     print('not saved. as no id found:', id)
        #     continue
        #
        # ajf = arl[0]
        # print('ajf.file_path', ajf.file_path)
        # if len(ajf.file_path) > 0 and ajf.file_path[0] == '\\':
        #     ajf.file_path = ajf.file_path[1:]
        # full_file_name = os.path.join(base_dir, ajf.file_path)
        save_amis_json_file_content(full_file_name, i['schema'])
        # if os.path.isfile(full_file_name):
        #
        #     print('saving file:', full_file_name)
        #     f = open(full_file_name, 'w', encoding='utf-8-sig')
        #     f.write(json.dumps(i['schema'], ensure_ascii=False))#.encode('utf-8')
        #     f.close()

    return HttpResponse('ok', status=200)

