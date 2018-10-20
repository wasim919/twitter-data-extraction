from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm, AppKeysForm
import pandas as pd
from .models import AppKeys
import tweepy
from twython import Twython


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
        uploaded_file_url = fs.url(username[5:])
        print('hi')
        print(uploaded_file_url)
        print('bye')
        usernames = read_username(username)
        dictio = {}
        appKeys = AppKeys.objects.all().order_by('-id')[0]
        consumer_key = appKeys.CustomerKey
        consumer_secret = appKeys.CustomerSecretKey
        access_token = appKeys.AccessTokenKey
        access_token_secret = appKeys.AccessTokenSecret
        file_url = []
        list1 = []
        dictio = {}
        for username in usernames:
            if len(username) != 0:
                file_url.append(fs.url('/document/'+username+'.txt'))
                twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
                output = twitter.lookup_user(screen_name=username)
                userid =  output[0]["id_str"]
                userid = int(userid)
                ids = get_followers_ids(userid, consumer_key, consumer_secret, access_token, access_token_secret)
                list2=[]
                file_to_write = 'media/document/'+username + ".txt"
                with open (file_to_write, 'w') as f:
                    for id in ids:
                        list2.append(str(id))
                        str_to_write = str(id) + "\n"
                        f.write(str_to_write)
                print ("Number of users found: " + str(len(ids)))
                list1.append(list2)
        dictio = dict(zip(file_url, list1))
        return render(request, 'part_1/followers.html', {
            'followers': dictio
            })
    return render(request, 'part_1/index.html')

def getKeys(request):
    if request.method == 'POST':
        print(request.POST)
        app_keys_form = AppKeysForm(request.POST)
        if app_keys_form.is_valid():
            app_keys_form.save()
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
