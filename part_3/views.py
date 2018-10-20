from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from part_1.models import AppKeys
import tweepy
from twython import Twython
import json
import pprint
from datetime import datetime
from tweepy.parsers import RawParser

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

def send_direct_message(dest, msg):
        event = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": dest
                    },
                    "message_data": {
                        "text": msg
                    }
                }
            }
        }
        api.send_direct_message_new(event)


def send_messages(list1, usernames, msg):
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    for username in usernames:
        print (username)
        try:
            if len(str(username)) > 0:
                output = twitter.lookup_user(screen_name=username)
                userid =  output[0]["id_str"]
                list1.append(username)
                userid = int(userid)
                send_direct_message(dest = userid, msg = msg)
                print ("message sent")
            else:
                continue
        except tweepy.TweepError as e:
            print (e)
            list2.append(username)
            print ("User not your friend")
            continue


def comment_on_profile(list1, usernames, comment):
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    for username in usernames:
        if len(str(username)) > 0:
            list1.append(username)
            print (username)
            m = "@%s " %(username)
            m = m + comment
            s= api.update_status(m)
            print('hi')
    return


def get_followers_ids(user_id):

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


def sendFollowerMessage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('media/document/'+ myfile.name, myfile)
        usernames=[]
        flw_users = read_username(filename)
        for users in flw_users:
            temp_array = []
            temp_array = get_followers_ids(users)
            usernames = usernames + temp_array
            print ("Number of users found: " + str(len(usernames)))
        list1 = []
        list2 = []
        message = request.POST.get('message')
        send_messages(list1, usernames = usernames, msg = message)
        print('hello')
        return render(request, 'part_3/sentFollowerMessage.html', {
        'message': message,
        'list1': list1,
        'list2': list2
        })
    else:
        return render(request, 'part_3/sendFollowerMessage.html')

def sendFollowerComment(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('media/document/'+ myfile.name, myfile)
        usernames=[]
        flw_users = read_username(filename)
        for users in flw_users:
            temp_array = []
            temp_array = get_followers_ids(users)
            usernames = usernames + temp_array
            print ("Number of users found: " + str(len(usernames)))
        list1 = []
        comment = request.POST.get('message')
        comment_on_profile(list1, usernames, comment)
        print('hello')
        return render(request, 'part_3/sentFollowerComment.html', {
        'message': comment,
        'list1': list1
        })
    else:
        return render(request, 'part_3/sendFollowerMessage.html')
