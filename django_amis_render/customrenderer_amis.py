__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"
'''
自定义返回处理
'''

# 导入控制返回的JSON格式的类
from rest_framework.renderers import JSONRenderer


class customrenderer_amis(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            # 如果返回的data为字典
            if isinstance(data, dict):
                # 响应信息中有message和code这两个key，则获取响应信息中的message和code，并且将原本data中的这两个key删除，放在自定义响应信息里
                # 响应信息中没有则将msg内容改为请求成功 code改为请求的状态码
                msg = data.pop('message', None)
                if msg is None:
                    msg = data.pop('msg', '请求成功')
                code = data.pop('code', renderer_context["response"].status_code)
                if 'results' in data:
                    data['items'] = data['results']
                    #del data['results']
                if 'count' in data:
                    data['total'] = data['count']
                    del data['count']

            # 如果不是字典则将msg内容改为请求成功 code改为请求的状态码
            else:
                msg = '请求成功'
                code = renderer_context["response"].status_code

            if code==403:
                msg = '权限错误：需要重新登录? '
                if 'detail' in data:
                    msg = msg + str(data['detail'])


            # 自定义返回的格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


class customrenderer_amis_release(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            # 如果返回的data为字典
            if isinstance(data, dict):
                # 响应信息中有message和code这两个key，则获取响应信息中的message和code，并且将原本data中的这两个key删除，放在自定义响应信息里
                # 响应信息中没有则将msg内容改为请求成功 code改为请求的状态码
                msg = data.pop('message', None)
                if msg is None:
                    msg = data.pop('msg', '请求成功')
                code = data.pop('code', renderer_context["response"].status_code)
                if 'results' in data:
                    data['items'] = data['results']
                    #delete results in release
                    del data['results']
                if 'count' in data:
                    data['total'] = data['count']
                    del data['count']

            # 如果不是字典则将msg内容改为请求成功 code改为请求的状态码
            else:
                msg = '请求成功'
                code = renderer_context["response"].status_code

            if code==403:
                msg = '权限错误：需要重新登录? '
                if 'detail' in data:
                    msg = msg + str(data['detail'])


            # 自定义返回的格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
