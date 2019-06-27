import os
import uuid, datetime
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from PIL.Image import Image
from .models import Post
from .forms import PostForm, SearchForm
from django.db.models import Q
from hackathon.settings import MEDIA_ROOT
from django.views.generic import View

# Create your views here.

#ホーム画面のビュー.　｛｝内に受け渡す変数を宣言
def home(request):
    today = datetime.datetime.now()
    month = []
    day = []
    weekday = []
    for n in range(7):
        month.append((today+datetime.timedelta(days=n)).month)
        day.append((today+datetime.timedelta(days=n)).day)
        weekday.append((today+datetime.timedelta(days=n)).weekday())
    if weekday[0]==0:
        weekday_char = [u'月', '火', u'水', u'木', u'金', u'土', u'日']
    elif weekday[0]==1:
        weekday_char = [u'火', u'水', u'木', u'金', u'土', u'日', u'月']
    elif weekday[0]==2:
        weekday_char = [u'水', u'木', u'金', u'土', u'日', u'月', '火']
    elif weekday[0]==3:
        weekday_char = [u'木', u'金', u'土', u'日', u'月', '火', u'水']
    elif weekday[0]==4:
        weekday_char = [u'金', u'土', u'日', u'月', '火', u'水', u'木']
    elif weekday[0]==5:
        weekday_char = [u'土', u'日', u'月', '火', u'水', u'木', u'金']
    else :
        weekday_char = [u'日', u'月', '火', u'水', u'木', u'金', u'土']
    
    if request.method == "GET":
        form = SearchForm()
        lo = u'東京'
        posts = Post.objects.all().order_by('-created_date')
        #weather API
        current_temp, daily_sky, max_temp, min_temp = wapi("Tokyo")
        
        daily_images = tenkiimage(daily_sky)#天気情報から天気の画像リンクを取得
        return render(request, 'clothes/home.html', {'form':form, 'posts':posts, 'max_temp':max_temp, 'min_temp':min_temp, 'current_temp':current_temp, 
            'daily_sky':daily_sky, 'day':day, 'month':month, 'weekday_char':weekday_char, 'daily_images':daily_images, 'lo':lo})
    elif request.method == "POST":
        form = SearchForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            lo = pref(request.POST.get('ken'))
            #weather API
            current_temp, daily_sky, max_temp, min_temp = wapi(request.POST.get('ken'))
            daily_images = tenkiimage(daily_sky)
            posts = Post.objects.filter(gender=request.POST.get('gender'), category=request.POST.get('category')
                ).filter(gender=request.POST.get('gender'), purpose=request.POST.get('purpose')
                ).order_by('-created_date')
            if max_temp[0]<=5 :
                posts = posts.filter(temp=u'~5')[:9]
            elif max_temp[0]<=10 :
                posts = posts.filter(temp=u'6~10')[:9]
            elif max_temp[0]<=15 :
                posts = posts.filter(temp=u'11~15')[:9]
            elif max_temp[0]<=20 :
                posts = posts.filter(temp=u'16~20')[:9]
            elif max_temp[0]<=25 :
                posts = posts.filter(temp=u'21~25')[:9]
            elif max_temp[0]<=30 :
                posts = posts.filter(temp=u'26~30')[:9]
            elif max_temp[0]>30 :
                posts = posts.filter(temp=u'31~')[:9]
    return render(request, 'clothes/home.html', {'form':form, 'data':data, 'posts':posts, 'max_temp':max_temp, 'min_temp':min_temp, 'current_temp':current_temp, 
        'daily_sky':daily_sky, 'daily_images':daily_images, 'day':day, 'month':month, 'weekday_char':weekday_char, 'lo':lo})

def toukou(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.image = request.FILES['image']
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'clothes/toukou.html', {'form':form})

#テスト用
# def search(request):
#     form = SearchForm()
#     if request.method == "GET":
#         return render(request, 'clothes/search.html', {'form':form})
#     elif request.method == 'POST':
#         form = SearchForm(request.POST)
#         posts = Post.objects.all()
#         if form.is_valid():
#             posts = posts.filter(Q(gender=form.cleaned_data['gender']), 
#                 Q(purpose=form.cleaned_data['purpose']), 
#                 Q(ken=form.cleaned_data['ken']), 
#                 ).order_by('-created_date')
#     return render(request, 'search.html', {'form':form, 'posts':posts})

def wapi(location):
        location_dict = {}
        location_dict['Tokyo'] = '1850147'
        location_dict['Kobe'] = '1859171'
        location_dict['Niigata'] = '1851951'
        location_dict['Sapporo'] = '2128295'
        location_dict['Yamanashi'] = '1861454'
        location_dict['Fukuoka'] = '1852915'
        location_dict['Ibaraki'] = '2112572'
        location_dict['Mie'] = '1849796'
        location_dict['Miyagi'] = '211277'
        location_dict['Oita'] = '1864750'
        location_dict['Wakayama'] = '1851426'
        location_dict['Hiroshima'] = '1857334'
        location_dict['Osaka'] = '1850034'
        location_dict['Shizuoka'] = '1851717'
        location_dict['Okayama'] = '1855416'
        location_dict['Aichi'] = '1856057'
        location_dict['Kanagawa'] = '1859642'
        location_dict['Iwate'] = '2111834'
        location_dict['Saitama'] = '1859740'
        location_dict['Okinawa'] = '1894616'
        location_dict['Chiba'] = '2113015'
        location_dict['Kyoto'] = '1857910'
        location_dict['Fukushima'] = '2112923'
        location_dict['Toyama'] = '1849876'
        location_dict['Tokushima'] = '1850158'
        location_dict['Gifu'] = '1863641'
        location_dict['Yamagata'] = '2110556'
        location_dict['Aomori'] = '2130658'
        location_dict['Nagasaki'] = '1856177'
        location_dict['Tottori'] = '1849892'
        location_dict['Tochigi'] = '1850311'
        location_dict['Yamaguchi'] = '1848689'
        location_dict['Akita'] = '2128867'
        location_dict['Gunma'] = '1857843'
        location_dict['Ishikawa'] = '1860243'
        location_dict['Fukui'] = '1863985'
        location_dict['Nagano'] = '1856215'
        location_dict['Shiga'] = '1853574'
        location_dict['Nara'] = '1855612'
        location_dict['Shimane'] = '1857550'
        location_dict['Kagawa'] = '1851100'
        location_dict['Ehime'] = '1926099'
        location_dict['Kouchi'] = '1859146'
        location_dict['Saga'] = '1860063'
        location_dict['Kumamoto'] = '1858421'
        location_dict['Miyazaki'] = '1856717'
        location_dict['Kagoshima'] = '1860827'
        
        
        import urllib.request
        import json
        import datetime
        today = datetime.date.today()
        tsuki = int(today.month)
        hi = int(today.day)
        
        key = '7608bc173f7b4f2b30d704fe6c938d32'
        day = '6' # forecast for day days (1 to ?)
        url_forecast = 'http://api.openweathermap.org/data/2.5/forecast/daily?id={0}&units=metric&cnt={1}&appid={2}'.format(location_dict[location], day, key)
        url_today = 'http://api.openweathermap.org/data/2.5/weather?id={0}&units=metric&appid={1}'.format(location_dict[location], key)
        response_forecast, response_today = urllib.request.urlopen(url_forecast), urllib.request.urlopen(url_today)
        data_forecast, data_today = response_forecast.read().decode('utf8'), response_today.read().decode('utf8')
        weather_info_forecast, weather_info_today = json.loads(data_forecast), json.loads(data_today)
        
        cnt_data_forecast = weather_info_forecast['cnt']
        city_data_forecast = weather_info_forecast['city']
        weather_data_forecast = weather_info_forecast['list']
        message_data_forecast = weather_info_forecast['message']
        cod_data_forecast = weather_info_forecast['cod']
        
        coord_data_today = weather_info_today['coord']
        base_data_today = weather_info_today['base']
        wind_data_today = weather_info_today['wind']
        cod_data_today = weather_info_today['cod']
        id_data_today = weather_info_today['id']
        weather_data_today = weather_info_today['main']
        sky_data_today = weather_info_today['weather']
        # その他多数
        
        daily_temp = []
        daily_temp.append(weather_data_today)
        for i in range(int(day)):
            p = weather_data_forecast[i]
            daily_temp.append(p)
        
        daily_sky = []
        daily_sky.append(sky_data_today[0]['description'])
        for i in range(int(day)):
            daily_sky.append(daily_temp[i+1]['weather'][0]['description'])
        	
        current_temp = daily_temp[0]['temp']
        max_temp = []
        min_temp = []
        max_temp.append(daily_temp[0]['temp_max'])
        min_temp.append(daily_temp[0]['temp_min'])
        for i in range(int(day)):
            max_temp.append(daily_temp[i+1]['temp']['max'])
            min_temp.append(daily_temp[i+1]['temp']['min'])
        max_temp1 = []
        min_temp1 = []
        for temp in max_temp:
            max_temp1.append(int(round(temp, 0)))
        for temp in min_temp:
            min_temp1.append(int(round(temp, 0)))
        current_temp = round(current_temp, 0)
        
        # daily_sky を日本語に変換
        for i in range(7):
            if daily_sky[i] == 'sky is clear':
                daily_sky[i] = '晴れ'
            elif daily_sky[i] == 'light rain':
                daily_sky[i] = 'くもり'
            elif daily_sky[i] == 'moderate rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'very heavy rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'heavy intensity rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'light intensity shower rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'few clouds':
                daily_sky[i] = 'くもり'
            elif daily_sky[i] == 'scattered clouds':
                daily_sky[i] = 'くもり'
            elif daily_sky[i] == 'broken clouds':
                daily_sky[i] = 'くもり'
            elif daily_sky[i] == 'overcast clouds':
                daily_sky[i] = 'くもり'
            elif daily_sky[i] == 'clear sky':
                daily_sky[i] = '晴れ'
            elif daily_sky[i] == 'shower rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'rain':
                daily_sky[i] = '雨'
            elif daily_sky[i] == 'thunderstorm':
                daily_sky[i] = '雷雨'
            elif daily_sky[i] == 'snow':
                daily_sky[i] = '雪'
            elif daily_sky[i] == 'mist':
                daily_sky[i] = '小雨'
            
        
        return current_temp, daily_sky, max_temp1, min_temp1
        
        #print('今日の天気: ' + str(daily_sky[0]))
        #print('現在の気温は' + str(current_temp) + 'です')
        #print('今日の最高気温は' + str(max_temp[0]) + 'です')
        #print('今日の最低気温は' + str(min_temp[0]) + 'です\n')
        #for i in range(int(day)):
            #print(str(tsuki) + '月' + str(hi + i + 1) + '日の天気: ' + str(daily_sky[i+1]))
            #print('最高気温は' + str(max_temp[i+1]) + 'です')
            #print('最低気温は' + str(min_temp[i+1]) + 'です\n')
        
        # daily_sky[] : 0～6に今日から6日先までの天気が入っている e.g. scattered cloud
        # current_temp : 現在の気温
        # max_temp[] : 0~6に今日から6日先までの最高気温が入っている
        # min_temp[] : 0~6に今日から6日先までの最低気温が入っている

def tenkiimage(sky):
    images =[]
    for sky in sky:
        if sky=='晴れ':
            images.append('tenki_images/kaisei.jpg')
        elif sky=='小雨':
            images.append('tenki_images/kosame.jpg')
        elif sky=='雨':
            images.append('tenki_images/ame.jpg')
        elif sky=='くもり':
            images.append('tenki_images/kumori.jpg')
        elif sky=='雷雨':
            images.append('tenki_images/raiu.jpg')
        elif sky=='雪':
            images.append('tenki_images/yuki.jpg')
    
    return images

def pref(ken):#POSTデータから日本語件名を取得
    kenmei = {
        u'Sapporo':u'北海道',
        u'Aomori':u'青森県',
        u'Iwate':u'岩手県',
        u'Miyagi':u'宮城県',
        u'Akita':u'秋田県',
        u'Yamagata':u'山形県',
        u'Fukushima':u'福島県',
        u'Ibaraki':u'茨城県',
        u'Tochigi':u'栃木県',
        u'Gunma':u'群馬県',
        u'Saitama':u'埼玉県',
        u'Chiba':u'千葉県',
        u'Tokyo':u'東京都',
        u'Kanagawa':u'神奈川県',
        u'Niigata':u'新潟県',
        u'Toyama':u'富山県',
        u'Ishikawa':u'石川県',
        u'Fukui':u'福井県',
        u'Yamanashi':u'山梨県',
        u'Nagano':u'長野県',
        u'Gifu':u'岐阜県',
        u'Shizuoka':u'静岡県',
        u'Aichi':u'愛知県',
        u'Mie':u'三重県',
        u'shiga':u'滋賀県',
        u'Kyoto':u'京都府',
        u'Osaka':u'大阪府',
        u'Kobe':u'兵庫県',
        u'Nara':u'奈良県',
        u'Wakayama':u'和歌山県',
        u'Tottori':u'鳥取県',
        u'Shimane':u'島根県',
        u'Okayama':u'岡山県',
        u'Hiroshima':u'広島県',
        u'Yamaguchi':u'山口県',
        u'Tokushima':u'徳島県',
        u'Kagawa':u'香川県',
        u'Ehime':u'愛媛県',
        u'Kouchi':u'高知県',
        u'Fukuoka':u'福岡県',
        u'Saga':u'佐賀県',
        u'nagasaki':u'長崎県',
        u'Kumamoto':u'熊本県',
        u'Oita':u'大分県',
        u'Miyazaki':u'宮崎県',
        u'Kagoshima':u'鹿児島県',
        u'Okinawa':u'沖縄県',
    }
    return kenmei[ken]
