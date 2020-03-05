from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
import requests
from django.views import View
from helloword import settings
import yaml, os, json
from juhe.models import User1


# Create your views here.

def qq(request):
    url = 'http://japi.juhe.cn/qqevaluate/qq'
    key = '595a3532a9bde28707b9e4b72f2a1869'
    qq = request.GET.get('qq')
    res = requests.get(f'{url}?key={key}&qq={qq}')
    return HttpResponse(res.text)


def image(request):
    filepath = os.path.join(settings.BASE_DIR, 'static/b.jpg')
    f = open(filepath, 'rb')
    return FileResponse(f, content_type='image/jpg')


class Image(View):

    def get(self, request):
        filepath = os.path.join(settings.BASE_DIR, 'static/c.jpg')
        f = open(filepath, 'rb')
        return FileResponse(f, content_type='image/jpg')
        # return render(request, 'uprile.html')

    def post(self, request):
        img = request.FILES
        for key, value in img.items():
            with open(f'static/{key[-8:]}', 'wb') as f:
                f.write(value.read())
        return HttpResponse('jjjj')

    def delete(self, request):
        picname = request.GET.get('name')
        print(picname)
        os.remove(f'static/{picname}')
        return picname


def jack(request):
    with open(r'D:\pythonProject\django_web\helloword\helloword\jkl.yaml', 'r', encoding='utf8') as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
    return JsonResponse(res, safe=False)


class TestCookie(View):
    def get(self, request):
        request.session['mykey'] = '我的值'
        return JsonResponse({'key': 'value'})


class TestCookie1(View):
    def get(self, request):
        print(request.session['mykey'])
        return JsonResponse({'key': 'value'})


class Authorize(View):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        # print(request.body)
        body = request.body.decode('utf8')
        bodydict = json.loads(body)
        code = bodydict.get('code')
        nickname = bodydict.get('nickname')
        appid = 'wx5e875597b62ce7cc'
        secret = 'f802f235c798601274c33188977c989e'
        # print(code)
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
        res = requests.get(url)
        res_dict = json.loads(res.text)
        openid = res_dict.get('openid')
        if not openid:
            return HttpResponse('fail')
        request.session['openid'] = openid
        request.session['is_authorized'] = True
        if not User1.objects.filter(openid=openid):
            newUser1 = User1(openid=openid, nickname=nickname)
            newUser1.save()

        return HttpResponse('ok')


class User(View):
    def get(self, request):
        openid = request.session.get('openid')
        user = User1.objects.get(openid=openid)
        city = json.loads(user.focus_cities)
        stock = json.loads(user.focus_stocks)
        constellation = json.loads(user.focus_constructions)
        return JsonResponse({
            'focus': {'constellation': constellation,
                      'city': city,
                      'stock': stock}
        })
        pass

    def post(self, request):
        openid = request.session.get('openid')
        user = User1.objects.get(openid=openid)
        body = request.body.decode('utf8')
        bodydict = json.loads(body)
        city = bodydict.get('city')
        stock = bodydict.get('stock')
        constellation = bodydict.get('constellation')
        user.focus_cities = json.dumps(city)
        user.focus_stocks = json.dumps(stock)
        user.focus_constructions = json.dumps(constellation)
        user.save()
        print(bodydict)
        return HttpResponse('ok')

    # def delete(self, request):
    #     pass


class Logout(View):
    def get(self, request):
        request.session.clear()
        return HttpResponse('...')


def already_authorized(request):
    is_authorized = False
    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized


class Status(View):
    def get(self, request):
        res = request.session.get('is_authorized')
        print(res)
        if already_authorized(request):
            data = {'is_authorized': 1}
        else:
            data = {'is_authorized': 0}
        return JsonResponse(data, safe=False)


def weather(cityname):
    '''
    :param cityname: 城市名字
    :return: 返回实况天气
    '''
    key = '7d4924c1d4ef9ee3f22dbd731535fbc4'
    api = 'http://v.juhe.cn/weather/index'

    params = f'cityname={cityname}&dtype=&format=&key={key}'
    url = api + '?' + params
    # print(url)
    response = requests.get(url=url)
    data = json.loads(response.text)
    # print(data)
    result = data.get('result')
    realtime = result.get('today')
    # print(result)
    print(realtime)
    response = {}
    response['temperature'] = realtime.get('temperature')
    response['win'] = realtime.get('wind')
    response['weather'] = realtime.get('weather')
    print(response)
    return response


class Weather(View):
    def get(self, request):
        if not already_authorized(request):
            response = {'key': 2500}
        else:
            data = []
            openid = request.session.get('openid')
            user = User1.objects.filter(openid=openid)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = data
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = weather(city.get('city'))
            result['city_info'] = city
            data.append(result)
        response_data = {'key': 'post..'}
        return JsonResponse(data=response_data, safe=False)
