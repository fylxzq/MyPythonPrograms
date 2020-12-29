from time import *
import requests
import itchat
import time
def countday():
    lovedayStr = "2016-10-23"
    loveday = time.strptime(lovedayStr,"%Y-%m-%d")
    timeStamp1 = ((time.mktime(loveday)))
    nowTime = time.localtime()
    timeStamp2 = int(time.mktime(nowTime))
    days = (timeStamp2-timeStamp1)/(24*60*60)
    return int(days)
def send_news():
    try:
        my_friend = itchat.search_friends(name="宝贝")
        name = my_friend[0]["UserName"]
        message2 = str(get_news()[0])
        message1 = "爱你的第" + str(countday()) + "天"
        # message3 = "来自爱你的那个男孩"
        itchat.send("爱你的我又出现了",toUserName=name)
        itchat.send(message2, toUserName=name)
        itchat.send(message1, toUserName=name)
    except:
        itchat.send("爱你的我再次出现了",toUserName=name)
def get_news():
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    contents = r.json()["content"]
    translation = r.json()["translation"]
    return  contents,translation
if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    a = 1
    while(a > 0):
        nowTime = time.localtime()
        if(nowTime.tm_hour==5 and nowTime.tm_min==20):
            send_news()
            break
        else:
            time.sleep(10)
            a += 0




