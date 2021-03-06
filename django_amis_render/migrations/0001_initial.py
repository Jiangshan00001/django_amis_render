# Generated by Django 3.2.8 on 2021-11-01 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmisRenderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.TextField(blank=True, help_text='app_name内部的url', null=True)),
                ('file_path', models.TextField(blank=True, help_text='文件保存路径，相对于项目根目录的相对路径', null=True)),
                ('html_template', models.TextField(blank=True, null=True)),
                ('json_file_url', models.TextField(blank=True, help_text='用于获取json数据的url', null=True)),
                ('file_type', models.TextField(blank=True, help_text='supported file type: json or html', null=True)),
                ('app_name', models.TextField(blank=True, help_text='文件所在的app的名称', null=True)),
                ('url_name', models.TextField(blank=True, help_text='程序内部需要，不需要设置', null=True)),
                ('page_url_all', models.TextField(blank=True, help_text='带app的url，不需要设置', null=True)),
            ],
            options={
                'verbose_name_plural': 'AMIS-PAGE',
                'db_table': 'amis_render_list',
                'managed': True,
            },
        ),
    ]
