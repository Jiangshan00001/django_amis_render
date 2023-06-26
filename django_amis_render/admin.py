# coding:utf-8

#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html

from django.contrib import admin

from django_amis_render.get_url_from_name import get_url_from_name
from .models import AmisRenderList, AmisRenderApp
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from .amis_update import update_amis_editor_to_local, update_amis_local_to_editor_one_file, get_amis_json_file_path, get_amis_json_file_content
# Register your models here.

from .auto_add import auto_add, auto_del
from .auto_add_app import auto_add_app, update_read_from_autourls, update_write_to_autourls,update_auto_read_write

class AmisRenderAppAdmin(admin.ModelAdmin):
    change_list_template = "html/auto_add_app_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('auto_add_app_action/', self.auto_add_app_action),
            path('update_app_auto/<int:id>/', self.update_auto),
            path('update_app_read/<int:id>/', self.update_read),
            path('update_app_write/<int:id>/', self.update_write),
        ]
        return my_urls + urls

    def update_auto(self, request, id):
        print('update_auto', id)
        apps = AmisRenderApp.objects.filter(id=id).all()
        if len(apps)>0:
            msg = update_auto_read_write(apps[0].app_name)
            self.message_user(request, msg)
        return HttpResponseRedirect("../../")
    def update_read(self, request, id):
        print('update read', id)
        apps = AmisRenderApp.objects.filter(id=id).all()
        if len(apps)>0:
            msg = update_read_from_autourls(apps[0].app_name, 1)
            self.message_user(request, msg)

        return HttpResponseRedirect("../../")
    def update_write(self, request, id):
        print('update write', id)
        apps = AmisRenderApp.objects.filter(id=id).all()
        if len(apps)>0:
            msg = update_write_to_autourls(apps[0].app_name)
            self.message_user(request, msg)
        return HttpResponseRedirect("../../")

    def auto_add_app_action(self, request):
        add_cnt = auto_add_app()
        self.message_user(request, str(add_cnt))
        return HttpResponseRedirect("../")


    def button_link_auto(self, obj):
        if obj.page_count is None:
            return ''
        button_html = """<a  href="update_app_auto/%s/" > 自动更新 </a>"""%obj.id
        return format_html(button_html)

    def button_link_read(self, obj):
        if obj.page_count is None:
            return ''
        button_html = """<a  href="update_app_read/%s/" > 读 </a>""" % obj.id
        return format_html(button_html)

    def button_link_write(self, obj):
        if obj.page_count is None:
            return ''
        button_html = """<a  href="update_app_write/%s/" > 写 </a>""" % obj.id
        return format_html(button_html)


    button_link_auto.short_description = "自动"
    button_link_read.short_description = "从auto_urls.py读出"
    button_link_write.short_description = "写入auto_urls.py"

    list_display = ['id', 'app_name', 'page_count','button_link_auto', 'button_link_read', 'button_link_write' ]



class AmisRenderListAdmin(admin.ModelAdmin):

    change_list_template = "html/auto_add_list.html"
    list_filter = ('app_name',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('auto_add_action/', self.auto_add_action),
            path('auto_del_action/', self.auto_del_action),
            path('update_amis_editor_to_local/', self.amis_editor_to_local),
            path('amis_to_editor/<int:id>/', self.amis_to_editor),

            path('amis_to_editor_and_jump/<int:id>/', self.amis_to_editor_and_jump),
            path('amis_edit_api/<int:id>/', self.amis_edit_api),
        ]
        return my_urls + urls

    def amis_edit_api(self, request, id):
        arl = AmisRenderList.objects.get(id=id)
        app_name = arl.app_name
        url_name = arl.url_name
        file_path= arl.file_path
        id = arl.id
        amis_json_file_path = get_amis_json_file_path(id)
        cont = get_amis_json_file_content(amis_json_file_path)

        return render(request, "amis_edit_api.html", context={'file_path':file_path,'url_name':url_name,  'id':id,'file_content':cont})

    def amis_to_editor(self, request, id):
        return update_amis_local_to_editor_one_file(id)

    def amis_to_editor_and_jump(self, id):
        update_amis_local_to_editor_one_file(id)

        return HttpResponseRedirect("/static/amis-editor-demo/index.html")

    def amis_editor_to_local(self, request):
        """
        数据从前端传过来，在request.POST中，需要保存到对应的文件中
        eg:<QueryDict: {'store': ['{"pages":[{"id":"1","icon":"","path":"jihua","label":"jihua.json","schema":{"body":[{"type":"input-email","label":"邮箱","name":"email"}],"type":"page"}}],"theme":"default","asideFixed":true,"asideFolded":false,"offScreen":false,"addPageIsOpen":false,"preview":false,"isMobile":false,"schema":{"body":[{"type":"input-email","label":"邮箱","name":"email"}],"type":"page"}}']}>

        """
        update_amis_editor_to_local(request)
        print('update_amis_editor_to_local', request)
        return HttpResponseRedirect("../")

    def auto_add_action(self, request):
        add_cnt = auto_add()
        self.message_user(request, "自动添加文件数："+str(add_cnt))
        return HttpResponseRedirect("../")

    def auto_del_action(self, request):
        add_cnt = auto_del()
        self.message_user(request, "自动删除已经不存在文件的路径数：" + str(add_cnt))
        return HttpResponseRedirect("../")

    def no_find_url_name_message(self, request, id):
        self.message_user('未找到路径。请查看：APP:', AmisRenderList.app_name,'是否有在全局urls.py中注册urls，并且app内部的urls里有写 from .auto_urls import *')
        return HttpResponseRedirect("../../")

    def button_link_open(self, obj):

        link_addr_got, link_to = get_url_from_name(obj.url_name,obj.app_name)
        app_and_url_name =str(obj.app_name)+':'+str(obj.url_name)

        

        if link_addr_got:
            # 尝试成功，直接显示连接
            button_html = """<a class="changelink" href="%s">打开</a>""" % (link_to)
        else:
            link_to = ''
            button_html = """<a >未找到页面 %s. 请确认%s.urls.py设置到项目的urls.py中，且%s.urls.py 里面有 from .auto_urls import *</a>"""%(app_and_url_name, str(obj.app_name), str(obj.app_name))

        return format_html(button_html)

    button_link_open.short_description = "打开页面"

    def button_link_edit(self, obj):
        button_html = """<input type="button" value="编辑" onclick="update_amis_local_to_editor(%s)" />"""%obj.id
        return format_html(button_html)

    button_link_edit.short_description = "编辑JSON文件"

    def button_link_edit_api(self, obj):
        # 修改内部各组件的api initApi等
        button_html = """<a class="changelink" href="amis_edit_api/%s/">编API</a>""" % (obj.id,)
        return format_html(button_html)

    button_link_edit_api.short_description = "编辑API"

    #'file_path',
    list_display = ['id','app_name', 'page_url',  'file_type',  'button_link_edit','button_link_edit_api','button_link_open']
    #actions = [make_published]

    class Media:
        js = ('django_amis_render/jquery-3.6.0.min.js', 'django_amis_render/add_button.js')

admin.site.register(AmisRenderList, AmisRenderListAdmin)
admin.site.register(AmisRenderApp, AmisRenderAppAdmin)

