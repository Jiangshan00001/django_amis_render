#coding:utf-8
__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os
from .models import AmisRenderApp, AmisRenderList


from .auto_add import parse_one_auto_urls, get_app_path, get_app_auto_urls_path
from .auto_add import get_amis_files, add_one_file_to_table,generate_one_auto_urls, get_rcd_by_app_name






def update_auto_read_write(app_name):

    return ''

def update_read_from_autourls(app_name):
    """
    从app目录读取auto_urls.py,解析内部数据，并更新数据库
    :param app_name:
    :return:
    """
    #获取app的auto_urls.py的路径
    app_path = get_app_path(app_name)
    if app_path is None:
        return '找不到app(%s)的路径.'%(str(app_name),)
    app_auto_urls_path = os.path.join(app_path, 'auto_urls.py')
    if not os.path.exists(app_auto_urls_path):
        return '找不到app(%s)中的auto_urls.py文件(%s).'%(app_name, str(app_auto_urls_path))

    f=open(app_auto_urls_path,'r')
    auto_urls_content = f.read()
    f.close()

    #解析数据
    head_py_code, parsed_data = parse_one_auto_urls(app_name, auto_urls_content)

    aapps = AmisRenderApp.objects.filter(app_name=app_name).all()
    if len(aapps)==0:
        return '未找到app'

    aapp = aapps[0]
    if aapp.head_py_code != head_py_code:
        aapp.save()

    for i in parsed_data:
        arls = AmisRenderList.objects.filter(app_name=app_name, url_name=i['url_name']).all()
        if len(arls)==0:
            #需要新增记录
            arl = AmisRenderList()
        else:
            #需要修改记录
            arl = arls[0]
        arl.app_name = app_name
        arl.file_path = i['file_path']
        arl.page_url = i['page_url']
        arl.file_type = i['file_type']
        arl.json_file_url = i['json_file_url']
        arl.html_template = i['html_template']
        arl.json_render_dict = i['json_render_dict']
        arl.json_render_func = i['json_render_func']
        arl.url_name = i['url_name']

        arl.save()

    return '已保存:'+str(len(parsed_data))

def update_write_to_autourls(app_name):
    """
    # 更新记录，并根据记录生成auto_urls.py
    :param app_name:
    :return:
    """
    app_path = get_app_path(app_name)
    file_list = get_amis_files(app_path)
    if len(file_list)==0:
        return '未找到页面文件，无法更新路由'
    for i in file_list:
        add_one_file_to_table(i,app_name=app_name)

    app_urls = get_rcd_by_app_name(app_name)
    aras = AmisRenderApp.objects.filter(app_name=app_name).all()
    if len(aras)==0:
        return '未找到此app'


    str_to_write = generate_one_auto_urls(app_name, app_urls[app_name], aras[0].head_py_code)
    auto_urls_path = get_app_auto_urls_path(app_name)
    if auto_urls_path is None:
        return 'auto_urls.py 写入错误'
    f = open(auto_urls_path, 'w')
    f.write(str_to_write)
    f.close()
    return '成功写入文件auto_urls.py.'


def count_file_in_app_path(app_path):
    file_list = get_amis_files(app_path)
    return len(file_list)

def auto_add_app():
    from django.conf import settings

    xinzeng_cnt=0
    update_cnt=0

    for i in settings.INSTALLED_APPS:
        is_xinzeng=1
        a_all = AmisRenderApp.objects.filter(app_name=i).all()
        app_stat = None
        if len(a_all)>0:
            #已经存在
            app_stat = a_all[0]
            is_xinzeng=0
        else:
            xinzeng_cnt+=1
            app_stat = AmisRenderApp(app_name = i)

        app_path = get_app_path(i)
        if app_path is None:
            if is_xinzeng==0 and app_stat.page_count!=None:
                app_stat.page_count=None
                app_stat.save()
                update_cnt+=1
            elif is_xinzeng:
                app_stat.page_count=None
                app_stat.save()
            continue

        cnt = count_file_in_app_path(app_path)

        if is_xinzeng:
            app_stat.page_count=cnt
            app_stat.save()
        elif (is_xinzeng==0) and (app_stat.page_count!=cnt):
            app_stat.page_count = cnt
            app_stat.save()
            update_cnt += 1

    return '新增app:'+str(xinzeng_cnt)+'. 更新页面数量的APP:'+str(update_cnt)+'.'

