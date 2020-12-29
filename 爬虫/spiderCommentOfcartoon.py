import requests
from fake_useragent import UserAgent
import json
import os
import csv
import pandas as pd

def gethtml(url):
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    print(response.apparent_encoding)
    return response.text

def parseHtml(html):
    data = json.loads(html)
    data = data["result"]["list"]
    lst = []
    for i in data:
        author = i["author"]["uname"]
        content = i["content"]
        print(content)
        ctime = i["ctime"]
        disliked = i["disliked"]
        likes = i["likes"]
        score = i["user_rating"]["score"]
        if("user_season" in i):
            index = i["user_season"]["last_ep_index"]
        else:
            index = None
        lst_one = [author,ctime,likes,disliked,score,index,content]
        lst.append(lst_one)
    cursor = data[19]["cursor"]
    file_to_csv(lst)
    return cursor


def file_to_csv(lst):
    file_size = os.path.getsize("inputData/cartoon.csv")
    if (file_size == 0):
        name = ["作者", "时间", "踩", "赞","评分","所看话数","内容"]
        file_test = pd.DataFrame(columns=name, data=lst)
        file_test.to_csv("inputData/cartoon.csv", encoding="utf-8-sig", index=False)
    else:
        with open("inputData/cartoon.csv", "a+", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)
def main():
    url = "https://bangumi.bilibili.com/review/web_api/short/list?media_id=102392&folded=0&page_size=20&sort=0"
    html = gethtml(url)
    # cursor = parseHtml(html)
    # print(cursor)
    # for i in range(50):
    #     url = "https://bangumi.bilibili.com/review/web_api/short/list?media_id=102392&folded=0&page_size=20&sort=0"+"&cursor="+str(cursor)
    #     html = gethtml(url)
    #     cursor = parseHtml(html)


if __name__ == '__main__':
    main()