__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"


from django.contrib import admin
from django.urls import path, re_path
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.urls import re_path, path, include
from .default_list import default_list,no_find_url_name_message
from .jhtml_render import jhtml_render
from .amis_update import update_amis_local_to_editor, update_amis_editor_to_local
urlpatterns = [
    path('no_find_url_name/<int:id>/', no_find_url_name_message, name='django_amis_render_no_find_url_name'),
    path('default_list/', default_list, name='django_amis_render_default_list'),
    path('update_amis_local_to_editor/', update_amis_local_to_editor),
    path('update_amis_editor_to_local/', update_amis_editor_to_local),

    re_path('^jhtml/.*$', jhtml_render),
]

