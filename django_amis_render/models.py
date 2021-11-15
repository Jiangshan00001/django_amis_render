from django.db import models


# Create your models here.

class AmisRenderList(models.Model):
    file_path = models.TextField(blank=True, null=True, help_text='文件保存路径，相对于项目根目录的相对路径')
    html_template = models.TextField(blank=True, null=True, help_text='渲染json用的html模板文件，不填使用默认的')
    json_file_url = models.TextField(blank=True, null=True, help_text='用于获取json数据的url')
    file_type = models.TextField(blank=True, null=True, help_text='supported file type: json, temp_json or html')
    app_name = models.TextField(blank=True, null=True, help_text='文件所在的app的名称')
    url_name = models.TextField(blank=True, null=True, help_text='不需要设置。程序内部使用，用于reverse获取url')
    page_url_all = models.TextField(blank=True, null=True, help_text='带app的url，不需要设置.用于比较请求的path')
    page_url = models.TextField(blank=True, null=True, help_text='app_name内部的url, 用于注册url时使用')

    json_render_dict=models.TextField(blank=True, null=True, help_text='用于json文件渲染的参数')
    class Meta:
        managed = True
        verbose_name_plural = 'AMIS-PAGE'
        db_table = 'amis_render_list'


