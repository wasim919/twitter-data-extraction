from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm, AppKeysForm
import pandas as pd
from .models import AppKeys
import tweepy
from twython import Twython

# consumer_key = "at4Esg9twYr0uVm3JSZw3TTGA"
# consumer_secret = "D4XmTaq1Z0v1WggioCmAO8bNwVnir56ZZq1moUTWwanHSzC4kT"
# access_token = "760167659254190080-RrL0UoHrkD7QfnyWWosNasbyTYHUsK2"
# access_token_secret = "2C8TVpS8D3vDW4BgN5NVoxJPxw2Ncf1l0mhMrsyfNKbgg"

def get_followers_ids(user_id, consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)
    ids = []
    page_count = 0
    for page in tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages():
        page_count += 1
        print ('Getting page {} for followers ids'.format(page_count))
        ids.extend(page)

    return ids

def read_username(filename):
    username = []
    with open (filename) as f:
        for line in f:
            line = line.strip()
            username.append(line)
    return username

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        username = fs.save('media/document/'+ myfile.name, myfile)
        # print(username)
        uploaded_file_url = fs.url(username)
        usernames = read_username(username)
        #user = api.get_user(screen_name = username)
        #print (user)
        # namelist = []
        dictio = {}
        appKeys = AppKeys.objects.all().order_by('-id')[0]
        consumer_key = appKeys.CustomerKey
        consumer_secret = appKeys.CustomerSecretKey
        access_token = appKeys.AccessTokenKey
        access_token_secret = appKeys.AccessTokenSecret
        #AppKeys.objects.all().delete()
        file_url = []
        list1 = []
        dictio = {}
        for username in usernames:
            if len(username) != 0:
                print (username)
                file_url.append(fs.url('media/document/'+username+'.txt'))
                print(file_url)
                twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
                output = twitter.lookup_user(screen_name=username)
                userid =  output[0]["id_str"]
                userid = int(userid)
                ids = get_followers_ids(userid, consumer_key, consumer_secret, access_token, access_token_secret)
                list2=[]
                file_to_write = 'media/document/'+username + ".txt"
                # list10.append(file_to_write)
                with open (file_to_write, 'w') as f:
                    for id in ids:
                        list2.append(str(id))
                        str_to_write = str(id) + "\n"
                        f.write(str_to_write)
                print ("Number of users found: " + str(len(ids)))
                list1.append(list2)
        dictio = dict(zip(file_url, list1))
        print(dictio)
        #print(uploaded_file_url)
        # return render(request, 'part_1/index.html', {
        #     'uploaded_file_url': uploaded_file_url
        #     })
        return render(request, 'part_1/followers.html', {
            'followers': dictio
            })
    return render(request, 'part_1/index.html')

# def handle_uploaded_file(f):
#     with open('media/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def getKeys(request):
    if request.method == 'POST':
        print(request.POST)
        app_keys_form = AppKeysForm(request.POST)
        if app_keys_form.is_valid():
            app_keys_form.save()
            # return render(request, 'part_1/index.html')
            return render(request, 'part_1/buttons.html')
        else:
            app_keys_form = AppKeysForm()
            return render(request, 'part_1/twitter_form.html', {
                'form': app_keys_form
                })

    elif request.method == 'GET':
        app_keys_form = AppKeysForm()
        return render(request, 'part_1/twitter_form.html', {
            'form': app_keys_form
            })













# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('display_followers.html')
#     else:
#         form = DocumentForm()
#     return render(request, 'part_1/model_form_upload.html', {
#         'form': form
#     })
