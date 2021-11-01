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
    """

    """

    # 文件已存在，不再添加
    curr = AmisRenderList.objects.filter(file_path=file_path).all()
    if len(curr)>0:
        #already exist, just skip
        return 0

    app_name = None
    pt = pathlib.Path(file_path)
    path_parts = pt.parts
    for i in range(len(path_parts)):
        if (path_parts[i] == 'static') and (i != 0):
            app_name = path_parts[i - 1]

    if app_name is None:
        # 不添加没有app名字的文件
        return

    url_name = app_name +'_'+ pt.stem + '_' + pt.suffix[1:]



    curr = AmisRenderList()
    curr.file_path = file_path
    curr.file_type = 'json'
    curr.app_name = app_name
    curr.url_name = url_name

    #从问及那路径，获取

    #pos = front_path.rfind('/')
    #front_path=front_path[:pos]
    front_path = get_app_url_base('django_amis_render_default_list')
    if front_path is None:
        return 0



    curr.page_url= pathlib.Path(file_path).name[:-5]+'/'

    pos = file_path.find('static')
    curr.json_file_url ='/'+file_path[pos:]
    curr.json_file_url = curr.json_file_url.replace('\\','/')

    curr.html_template = None
    curr.save()
    return 1

def get_amis_files():
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
            if if_file_is_amis_json(file_name):
                amis_json_file_list.append(file_name)

    return amis_json_file_list

def update_rcd(amis_json_file_list):
    add_cnt=0
    for i in amis_json_file_list:
        add_len = add_one_file_to_table(i)
        add_cnt+=add_len

    return add_cnt


def get_rcd_by_app_name():
    """
    数据库中将数据读出，按照app_name分类
    """
    from django.forms.models import model_to_dict

    aml = AmisRenderList.objects.all().order_by('id')

    #{app_name1:[mod1,mod2,...],... }
    aml_app_dict={}
    for i in aml:
        ii = model_to_dict(i)
        if (ii['app_name'] is None) or (ii['app_name']==''):
            continue
        app_name = ii['app_name']
        if app_name not in aml_app_dict:
            aml_app_dict[app_name] = []
        aml_app_dict[app_name].append(ii)

    return aml_app_dict

def add_needed_urls():
    pass

def add_needed_auto_urls(aml_app_dict):
    # 生成auto_urls.py
    for i in aml_app_dict:
        app_name = i
        urls_mod = aml_app_dict[i]
        str_to_write='from django.urls import re_path, path\n'
        str_to_write+='import django_amis_render\n'
        str_to_write+='from .urls import urlpatterns\n'
        for j in urls_mod:
            str_to_write+= "urlpatterns.append(path('%s', django_amis_render.jhtml_render.jhtml_render, name='%s'))\n"%(j['page_url'], j['url_name'])

        app_path = os.path.join(settings.BASE_DIR, app_name)
        auto_urls_path = os.path.join(app_path, 'auto_urls.py')
        f=open(auto_urls_path,'w')
        f.write(str_to_write)
        f.close()

def load_urls_template():
    f=open(os.path.join(os.path.dirname(__file__), 'urls_template.py'),'r' )
    ret = f.read()
    f.close()
    return ret
def add_urls_needed(aml_app_dict):
    urls_temp_content = None
    for i in aml_app_dict:
        urls_py_path = os.path.join(os.path.join(settings.BASE_DIR, i),'urls.py')
        if os.path.exists(urls_py_path):
            continue
        if urls_temp_content is None:
            urls_temp_content = load_urls_template()

        f=open(urls_py_path,'w')
        f.write(urls_temp_content)
        f.close()

def auto_add():

    amis_json_file_list = get_amis_files()
    #print(amis_json_file_list)
    cnt = update_rcd(amis_json_file_list)

    aml_app_dict = get_rcd_by_app_name()

    add_needed_auto_urls(aml_app_dict)
    add_urls_needed(aml_app_dict)

    return cnt

def auto_del():
    cnt = 0
    amis_json_file_list = get_amis_files()

    for i in AmisRenderList.objects.all():
        if i.file_path not in amis_json_file_list:
            i.delete()
            cnt+=1

    return str(cnt)