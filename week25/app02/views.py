from django.shortcuts import render
import requests
# Create your views here.

def req(request):
    # 通过下面的方式，请求有django来发送，获取到数据再传递给浏览器。
    response = requests.get('http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101121301')
    # 注意传过来的是字节，我们需要将其用utf-8编码一下，不然传到前端就是乱码的
    response.encoding='utf-8'
    print(response.text)
    return render(request,'req.html',{'result':response.text})
