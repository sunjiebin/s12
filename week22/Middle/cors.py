from django.utils.deprecation import MiddlewareMixin

class cors(MiddlewareMixin):
    '''CORS中间件，允许来自http://127.0.0.1:8000的跨域请求，加上这个中间件后，
    服务器响应数据时，会在Response Hearders里面加上响应头：Access-Control-Allow-Origin:http://127.0.0.1:8000
    浏览器在接受到这个响应头之后，就会允许页面接受跨域请求的数据
    与week25里面的跨域请求结合测试使用
    '''
    def process_response(self,request,response):
        print(request)
        response['Access-Control-Allow-Origin']='http://127.0.0.1:8000'
        return response