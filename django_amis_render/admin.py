

#https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html

from django.contrib import admin
from .models import AmisRenderList
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse,HttpResponseRedirect

# Register your models here.

from .auto_add import auto_add

#@admin.action(description='自动添加json文件和路径')
#def make_published(modeladmin, request, queryset):
#    auto_add(request)

class AmisRenderListAdmin(admin.ModelAdmin):

    change_list_template = "html/auto_add_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('auto_add_action/', self.auto_add_action),
        ]
        return my_urls + urls


    def auto_add_action(self, request):
        auto_add(request)
        self.message_user(request, "OK")
        return HttpResponseRedirect("../")

    def button_link(self, obj):
        button_html = """<a class="changelink" href="%s">打开页面</a>"""%(obj.page_url)
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
