__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"
from django.urls import re_path, path, include
import traceback
urlpatterns = [
]


try:
    from .auto_urls import auto_urlpatterns
    urlpatterns.extend(auto_urlpatterns)
except Exception as e:
    print("from .auto_urls import auto_urlpatterns", e)
    traceback.print_exc()
