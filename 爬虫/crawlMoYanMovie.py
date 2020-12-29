import requests,time
import json,csv,os
from fake_useragent import UserAgent
import pandas as pd

class moyanSpider():
    headers = {
        "User-Agent": UserAgent(verify_ssl=False).random,
        "Host": "m.maoyan.com",
        "Referer": "http://m.maoyan.com/movie/1217236/comments?_v_=yes"
            }
    def __init__(self,url,time):
        self.time = time
        self.url = url

    def get_json(self):
        resopnse = requests.get(self.url,headers=self.headers)
        raw_data = resopnse.text
        json_data = json.loads(raw_data)
        return json_data

    def get_data(self,json_data):
        data = json_data["cmts"]
        lst_info = []
        for i in data:
            cityName = i["cityName"]
            content = i["content"]
            if "gender" in i:
                gender = i["gender"]
            else:
                gender = 0
            nickName = i["nickName"]
            userLevel = i["userLevel"]
            score = i["score"]
            list_one = [self.time,nickName,gender,cityName,
                        userLevel,score,content]
            lst_info.append(list_one)
        self.file_to(lst_info)
    def file_to(self,list_info):
        file_size = os.path.getsize("inputData/maoyan.csv")
        if(file_size==0):
            name = ["评论日期","昵称","性别","城市名","用户等级","评分","内容"]
            file_test = pd.DataFrame(columns=name,data=list_info)
            file_test.to_csv("inputData/maoyan.csv",encoding="utf-8-sig",index=False)
        else:
            with open("inputData/maoyan.csv","a+",encoding="utf-8-sig",newline="") as file:
                writer = csv.writer(file)
                writer.writerows(list_info)

def spider_maoyan():
    offset = 0
    startTime = "2018-09-21"
    day = [22,23,24,25,26,27,28,29,30,1,2,3,4,5,6]
    j = 0
    page_num = int(20000/15)
    for i in range(page_num):
        comment_api = 'http://m.maoyan.com/mmdb/comments/movie/1217236.json?_v_=yes&offset={0}&startTime={1}%2021%3A09%3A31'.format(offset,startTime)
        s0 = moyanSpider(comment_api,startTime)
        json_comment = s0.get_json()
        if(json_comment["total"]==0):
            if(j<9):
                startTime="2018-09-%d"%day[j]
            elif(j>=9 and j<15):
                startTime="2018-10-%d"%day[j]
            else:
                break
            offset = 0
            j = j+1
            continue
        s0.get_data(json_comment)
        offset = offset+15

if __name__:
    spider_maoyan()






