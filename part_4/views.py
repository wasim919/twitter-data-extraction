from django.shortcuts import render, redirect
import pandas as pd
import tweepy
from twython import Twython
import json
import pprint
from datetime import datetime
from tweepy.parsers import RawParser
from part_1.models import AppKeys
from django.core.files.storage import FileSystemStorage

# consumer_key = "c8y3bCLMg7a0YHdu9COojWHuV"
# consumer_secret = "mqQAcex01SdYsghMEpCASik9xt7CDgQsaJekLzQ9j7Sf6kEJlA"
# access_token = "746216532242399232-80x2w2prAxnZQ5UM1nc14zWsTpibAUc"
# access_token_secret = "41GS8NMnAKkINhyZq2cBX35ueAcS5ys82QiVxea6CL09A"

appKeys = AppKeys.objects.all().order_by('-id')[0]
consumer_key = appKeys.CustomerKey
consumer_secret = appKeys.CustomerSecretKey
access_token = appKeys.AccessTokenKey
access_token_secret = appKeys.AccessTokenSecret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)
RawParser = RawParser()


def read_username(filename):        #give the filename of the users who u want to follow

    username = []
    with open (filename) as f:
        for line in f:
            line = line.strip()
            username.append(line)
    return username






def requestfollow(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        username = fs.save('media/document/'+ myfile.name, myfile)
        uploaded_file_url = fs.url(username)
        usernames = read_username(username)
        list1 = []
        list2 = []
        for username in usernames:
            if len(username) != 0:
                print (username)
                twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
                output = twitter.lookup_user(screen_name=username)
                userid =  output[0]["id_str"]
                userid = int(userid)
                try:
                    api.create_friendship(userid)
                    list1.append(username)
                except tweepy.TweepError as e:
                    print (e)
                    list2.append(username)
                    pass
        return render(request, 'part_4/afterSend.html', {
        'requestC': list1,
        'requestNc': list2
        })
    elif request.method == 'GET':
        return render(request, 'part_4/send.html')
