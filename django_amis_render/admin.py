

#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html

from django.contrib import admin
from .models import AmisRenderList
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse,HttpResponseRedirect

# Register your models here.

from .auto_add import auto_add, auto_del

#@admin.action(description='自动添加json文件和路径')
#def make_published(modeladmin, request, queryset):
#    auto_add(request)

class AmisRenderListAdmin(admin.ModelAdmin):

    change_list_template = "html/auto_add_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('auto_add_action/', self.auto_add_action),
            path('auto_del_action/', self.auto_del_action),
        ]
        return my_urls + urls

    def no_find_url_name_message(self, request, id):
        self.message_user('未找到路径。请查看：APP:', AmisRenderList.app_name,'是否有在全局urls.py中注册urls，并且app内部的urls里有写 from .auto_urls import *')
        return HttpResponseRedirect("../../")

    def auto_add_action(self, request):
        add_cnt = auto_add()
        self.message_user(request, "自动添加文件数："+str(add_cnt))
        return HttpResponseRedirect("../")

    def auto_del_action(self, request):
        add_cnt = auto_del()
        self.message_user(request, "自动删除已经不存在文件的路径数：" + str(add_cnt))
        return HttpResponseRedirect("../")

    def button_link(self, obj):
        from django.urls import reverse
        try:
            link_to = reverse(obj.url_name)
            button_html = """<a class="changelink" href="%s">打开页面</a>""" % (link_to)
        except Exception as e:
            link_to=reverse('django_amis_render_no_find_url_name', args=[obj.id])
            button_html = """<a class="changelink" href="%s">未找到页面</a>"""%(link_to)
        return format_html(button_html)

    button_link.short_description = "打开"

    def button_link_edit(self, obj):
        button_html = """<a class="changelink" href="%s">编辑页面</a>"""%(obj.page_url)
        return format_html(button_html)

    button_link_edit.short_description = "编辑"

    list_display = ['id', 'page_url', 'file_path', 'button_link']
    #actions = [make_published]

    class Media:
        js = ('django_amis_render/jquery-3.6.0.min.js',)# 'django_amis_render/add_button.js')

admin.site.register(AmisRenderList, AmisRenderListAdmin)
