# Generated by Django 3.2.8 on 2021-11-22 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_amis_render', '0004_amisrenderapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='amisrenderapp',
            name='head_py_code',
            field=models.TextField(blank=True, help_text='auto_urls.py添加的py代码，一般用于引入模板参数函数', null=True),
        ),
        migrations.AddField(
            model_name='amisrenderlist',
            name='json_render_func',
            field=models.TextField(blank=True, help_text='用于json文件渲染的参数生成函数，入参只有一个request,出参是dict类型。如需导入，需要在AmisRenderApp的head_py_code中添加导入代码', null=True),
        ),
        migrations.AlterField(
            model_name='amisrenderlist',
            name='json_render_dict',
            field=models.TextField(blank=True, help_text='用于json文件渲染的参数，是json的dict字符串形式', null=True),
        ),
    ]
