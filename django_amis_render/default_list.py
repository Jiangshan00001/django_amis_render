__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from .models import AmisRenderList
from django.http import HttpResponse,HttpResponseRedirect



def default_list(request):
    #return HttpResponse()
    return 'ok'

def no_find_url_name_message(request, id):
    aml = AmisRenderList.objects.get(id=id)

    to_show_str = '<html> <body> <table> <tr><th>字段名</th> <th>内容</th></tr>'
    to_show_str += ' <tr> <th>id </th><th>' + str(aml.id) + '</th></tr>\n'
    to_show_str += '<tr> <th>file_path</th><th>' + str(aml.file_path) + '</th></tr>\n'
    to_show_str += '<tr> <th>app_name</th><th>' + str(aml.app_name) + '</th></tr>\n'
    to_show_str += '<tr> <th>url_name</th><th>' + str(aml.url_name) + '</th></tr> </table>\n'
    to_show_str += '可能问题：1. app_name的url未注册: 需要在项目urls.py中添加app_name 的url. <p>'
    to_show_str += '可能问题：2. app_name的urls.py中没有 from .auto_urls import * .\n<p>'

    to_show_str += '</body></html>\n'



    return HttpResponse(
        to_show_str
    )