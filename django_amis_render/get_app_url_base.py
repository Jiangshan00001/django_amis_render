__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.urls import reverse

def get_app_url_base(my_url_name='django_amis_render_default_list'):
    try:
        front_path = reverse(my_url_name)
    except Exception as e:
        print('get_app_url_base reverse. no url set?')
        return None

    if front_path[-1]=='/':
        front_path=front_path[:-1]

    pos = front_path.rfind('/')
    front_path=front_path[:pos]
    return front_path

