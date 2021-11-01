__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"
from django.urls import re_path, path, include
urlpatterns = [
]


try:
    from .auto_urls import *
except Exception as e:
    print(".auto_urls import * error", e)