__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.http import HttpResponse
from django.conf import settings
import os
from .models import AmisRenderList
import pathlib
from django.urls import reverse
from .get_app_url_base import get_app_url_base


def if_file_is_amis_json(file_path):
    if file_path[-4:]!='json':
        return False
    if 'amis_json' not in file_path:
        return False
    if 'static' not in file_path:
        return False
    return True


def add_one_file_to_table(file_path):
    curr = AmisRenderList.objects.filter(file_path=file_path).all()
    if len(curr)>0:
        #already exist, just skip
        return 0
    curr = AmisRenderList()
    curr.file_path = file_path
    curr.file_type = 'json'

    #front_path = reverse('django_amis_render_default_list')
    #if front_path[-1]=='/':
    #    front_path=front_path[:-1]

    #pos = front_path.rfind('/')
    #front_path=front_path[:pos]
    front_path = get_app_url_base('django_amis_render_default_list')
    if front_path is None:
        return 0

    curr.page_url=front_path+'/jhtml/'+pathlib.Path(file_path).name[:-5]

    pos = file_path.find('static')

    curr.json_file_url ='/'+file_path[pos:]
    curr.json_file_url = curr.json_file_url.replace('\\','/')



    curr.html_template = None
    curr.save()
    return 1

def auto_add():
    bdir = settings.BASE_DIR
    #找到目录下，所有目录名称为amis_json的目录，下面的 json文件，都添加路由
    amis_json_file_list = []
    print('auto_add bdir:', bdir)
    for root, dirs, files in os.walk(bdir, topdown=False):
        #print(root)
        blen = len(str(bdir))
        if str(bdir) == root[0:blen]:
            root=root[blen:]
        for name in files:
            file_name =os.path.join(root, name)
            #print(file_name)
            if if_file_is_amis_json(file_name):
                amis_json_file_list.append(file_name)

    #print(amis_json_file_list)
    add_cnt=0
    for i in amis_json_file_list:
        add_len = add_one_file_to_table(i)
        add_cnt+=add_len

    return add_cnt