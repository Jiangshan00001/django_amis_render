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


def get_app_path(app_name):
    # TODO: 当前只有在BASE_DIR中的app才会被搜索到，如果不在此目录下，则直接返回None
    from django.conf import settings
    bdir = settings.BASE_DIR
    app_path = os.path.join(bdir, app_name)
    if not os.path.exists(app_path):
        return None
    return app_path


def get_app_auto_urls_path(app_name):
    """
    获取指定app的auto_urls.py文件路径
    :param app_name:
    :return:
    """
    app_path = get_app_path(app_name)
    if app_path is None:
        return None
    auto_urls_path = os.path.join(app_path, 'auto_urls.py')
    return auto_urls_path

def if_file_is_amis_json(file_path):
    """
    判断文件是否是amis文件：根据文件路径 和后缀
    :param file_path:
    :return:
    """

    if file_path[-4:]!='json':
        return False
    if 'amis_json' not in file_path:
        return False
    if ('static' not in file_path) and ('templates' not in file_path):
        return False
    return True


def get_app_name_from_path(file_path):
    app_name = None
    pt = pathlib.Path(file_path)
    path_parts = pt.parts
    for i in range(len(path_parts)):
        if (path_parts[i] == 'static') and (i != 0):
            app_name = path_parts[i - 1]
            break
        if (path_parts[i] == 'templates') and (i != 0):
            app_name = path_parts[i - 1]
            break

    if app_name is None:
        # 不添加没有app名字的文件
        return
    return app_name


def get_file_type_from_path(file_path):
    """
    根据文件路径，返回文件类型
    :param file_path:
    :return:
    """
    app_name = get_app_name_from_path(file_path)

    file_type='unknown'
    json_file_url = ''
    file_path1 = file_path.replace('\\','/')
    pos = file_path1.find('static/')
    if pos < 0:
        pos = file_path1.find('templates/')
        if pos<0:
            return None
        # templates json文件的路由
        pos += 10
        json_file_url ='/'+ file_path[pos:]
        json_file_url = json_file_url.replace('\\','/')
        return 'temp_json', json_file_url
    else:
        json_file_url ='/'+file_path[pos:]
        json_file_url = json_file_url.replace('\\','/')
        return 'json', json_file_url

    return None, json_file_url

def get_file_path_from_json_file_url(app_name, file_type, json_file_url):
    if file_type=='json':
        pass
        return app_name+json_file_url
    elif file_type=='temp_json':
        return app_name+'/templates' + json_file_url

    return None

def add_one_file_to_table(file_path, app_name=None, force_to_default=0):
    """
    添加一个文件到table中，如果已经存在，则不添加
    :param file_path:
    :return:
    """

    # 文件已存在，不再添加
    curr = AmisRenderList.objects.filter(file_path=file_path).all()
    if len(curr)>0 and (not force_to_default):
        #already exist, just skip
        return 0
    elif len(curr)>0:
        curr = curr[0]
    else:
        curr = AmisRenderList()

    if app_name is None:
        app_name = get_app_name_from_path(file_path)

    if app_name is None:
        # 不添加没有app名字的文件
        return 0

    pt = pathlib.Path(file_path)
    url_name = pt.stem.replace('.', '_')

    curr.file_path = file_path
    curr.app_name = app_name
    curr.url_name = url_name
    curr.page_url= url_name+'/'
    #从问及那路径，获取

    curr.file_type,curr.json_file_url = get_file_type_from_path(file_path)

    curr.html_template = None
    curr.save()
    return 1

def get_amis_files(bdir=None):
    """
    传入路径，返回文件列表.如果传入None，则查找项目下所有的amis文件
    :param bdir:
    :return:['path_relative_to_settings.BASE_DIR_if_possible',...]
    """
    base_dir = settings.BASE_DIR
    if bdir is None:
        bdir = base_dir

    #找到目录下，所有目录名称为amis_json的目录，下面的 json文件，都添加路由
    amis_json_file_list = []
    print('auto_add bdir:', bdir)
    for root, dirs, files in os.walk(bdir, topdown=False):
        blen = len(str(base_dir))
        if str(base_dir) == root[0:blen]:
            root=root[blen:]
            if len(root)>0 and (root[0]=='/' or root[0]=='\\'):
                root=root[1:]
        for name in files:
            file_name =os.path.join(root, name)
            if if_file_is_amis_json(file_name):
                # 所有文件路径，都改为/
                file_name=file_name.replace('\\','/')
                amis_json_file_list.append(file_name)

    return amis_json_file_list

def update_rcd(amis_json_file_list):
    """
    根据传入的文件列表，更新记录
    """
    add_cnt=0
    for i in amis_json_file_list:
        add_len = add_one_file_to_table(i)
        add_cnt+=add_len

    return add_cnt


def get_rcd_by_app_name(app_name=None):
    """
    数据库中将数据读出，按照app_name分类
    :param app_name:如果是None，则返回所有的app的，否则返回指定的app的
    :return: {app_name:[url1,url2...], }
    """
    from django.forms.models import model_to_dict

    if app_name==None:
        aml = AmisRenderList.objects.all().order_by('id')
    else:
        aml = AmisRenderList.objects.filter(app_name=app_name).all().order_by('id')

    #{app_name1:[mod1,mod2,...],... }
    aml_app_dict={}
    for i in aml:
        ii = model_to_dict(i)
        if (ii['app_name'] is None) or (ii['app_name']==''):
            continue

        for kk in ii:
            if ii[kk]=='' or  ii[kk]=='None':
                # 如果是空字符串，或字符串None,则改为None. 解决在修改保存时，json_render_dict=‘’的错误问题
                ii[kk] =None

        app_name = ii['app_name']
        if app_name not in aml_app_dict:
            aml_app_dict[app_name] = []
        aml_app_dict[app_name].append(ii)

    return aml_app_dict



def parse_one_auto_urls(app_name, urls_content):
    urls_lines = urls_content.split('\n')

    status='head'
    head_py_code=''
    url_mods=[]
    for one_line in urls_lines:
        if len(one_line)==0:
            #空行
            continue
        if one_line[0] == '#':
            #注释行
            continue
        if status=='head':
            if 'auto_urlpatterns=[' in one_line:
                #转移状态，改为解析路由
                status = 'patterns'
                continue
            head_py_code += one_line+'\n'

        if status=='patterns':
            #path('login/', lambda req: jhtml_render(request=req,file_type ='json', json_file_url='/static/amis_json/login.json', html_template=None,  render_var_dict_str=None, render_var_dict_func=None), name='login'),
            parts = one_line.split(',')
            if len(parts)<9:
                #当前解析后，有9个字符串，如果编码格式有改变，此处需要修改
                continue
            if 'render_template_json' in parts[1]:
                continue
            parts = [ i.strip() for i in parts]
            if "path('" not in parts[0]:
                continue
            #path('%s', lambda req: jhtml_render(request=req, --01
            # file_type=%r,  -2
            # json_file_url=%r, -3
            # html_template=%r,   -4
            # json_render_dict=%s, -5
            # json_render_func=%s, -6
            # file_path=%r,        -7
            # url_name=%r,         -8
            # app_name=%r),        -9
            # name='%s'), \n" % (  -10
            j={}
            j['page_url']=parts[0][6:-1]
            j['file_type']=parts[2].split('=')[1].replace("'",'')
            j['json_file_url'] = parts[3].split('=')[1].replace("'", '')
            j['html_template'] = parts[4].split('=')[1].replace("'", '')

            j['json_render_dict'] = parts[5].split('=')[1].replace("'", '')
            j['json_render_func'] = parts[6].split('=')[1].replace("'", '').replace(')', '')
            j['file_path'] = parts[7].split('=')[1].replace("'", '').replace(')', '')
            j['url_name'] = parts[8].split('=')[1].replace("'", '').replace(')', '')
            j['app_name'] = parts[9].split('=')[1].replace("'", '').replace(')', '')
            for kk in j:
                if j[kk]=='None':
                    j[kk] = None

            url_mods.append(j)

    return head_py_code, url_mods



def generate_one_auto_urls(app_name, urls_mod, head_py_code=None):
    str_to_write = ''
    str_to_write += '#coding:utf-8\n'
    str_to_write += '# THIS IS A AUTO-GENERATED FILE. DO NOT EDIT THIS FILE MANUALLY\n'
    str_to_write += '# EDIT in web: /admin/django_amis_render/amisrenderlist/  \n'
    str_to_write += '#            and this file will change accordingly\n'

    if head_py_code is not None:
        str_to_write += head_py_code+'\n'
    else:
        #default head_py_code
        str_to_write += 'from django.urls import re_path, path\n'
        str_to_write += 'from django_amis_render.jhtml_render import jhtml_render, render_template_json\n'
        

    str_to_write += '\n'
    str_to_write += 'auto_urlpatterns=[\n'

    for j in urls_mod:
        ######################
        # 此处生成1个路由
        # 如果此处有修改，则parse_one_auto_urls 函数也可能需要相应的修改，才能正常解析数据
        str_to_write += "    path('%s', lambda req: jhtml_render(request=req,file_type=%r, json_file_url=%r, html_template=%r,  json_render_dict=%s, json_render_func=%s, file_path=%r, url_name=%r, app_name=%r), name='%s'), \n" % (
        j['page_url'], j['file_type'], j['json_file_url'], j['html_template'], j['json_render_dict'], j['json_render_func'], j['file_path'],   j['url_name'], j['app_name'], j['url_name'])
        # 如果是template的json，则需要单独的模板渲染路由
        if j['file_type'] == 'temp_json':
            str_to_write += "    path('%s', lambda req: render_template_json(request=req, file_path=%r,json_render_dict=%s, json_render_func=%s ), name='%s'), \n" % (
            j['page_url'] + 'tjson/', j['file_path'],  j['json_render_dict'],j['json_render_func'],           j['url_name'] + '_tjson')

    str_to_write += ']#auto_urlpatterns end\n'
    str_to_write += '\n'
    return str_to_write

def add_needed_auto_urls(aml_app_dict):
    """
    生成auto_urls.py
    :param aml_app_dict:{app_name1[url1,url2,...], ...}
    :return:
    """
    from .models import AmisRenderApp
    for i in aml_app_dict:
        app_name = i
        urls_mod = aml_app_dict[i]

        aras = AmisRenderApp.objects.filter(app_name=app_name).all()
        head_py_code=None
        if len(aras)>0:
            head_py_code=aras[0].head_py_code

        str_to_write = generate_one_auto_urls(app_name, urls_mod,head_py_code)

        auto_urls_path = get_app_auto_urls_path(app_name)
        f=open(auto_urls_path,'w')
        f.write(str_to_write)
        f.close()

def load_urls_template():
    """
    获取urls.py模板文件内容
    :return:
    """
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
    """
    自动添加
    1 查找所有amis文件
    2 更新记录
    3 记录按照app组织，生成dict
    4 为每个app生成auto_urls.py
    :return:
    """

    amis_json_file_list = get_amis_files()
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

def add_needed_urls():
    pass