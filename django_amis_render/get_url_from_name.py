

from django.urls import reverse


def get_url_from_name(url_name, app_name):
    """
    根据url的名称和app的名称，获取对应的连接路径
    """
    link_addr_got = False
    link_to = '/nowhere'
    # 尝试获取连接地址：方式1
    try:
        app_and_url_name =str(app_name)+':'+str(url_name)
        link_to = reverse(app_and_url_name)
        link_addr_got = True
    except Exception as e:
        link_addr_got = False

    # 如果方式1失败，则尝试第二种方式:
    if not link_addr_got:
        try:
            link_to = reverse(str(url_name), current_app=app_name)
            link_addr_got = True
        except Exception as e:
            link_addr_got = False

    return link_addr_got, link_to
        