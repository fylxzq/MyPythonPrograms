import os

import requests
from bs4 import BeautifulSoup
import base64
import csv
import pandas as pd

def getCityLst():
    citylst = []
    url = "http://www.creprice.cn/proprice/pchebei.html"
    respnse = requests.get(url)
    respnse.encoding = respnse.apparent_encoding
    html = respnse.text
    soup = BeautifulSoup(html,"html.parser")
    ul = soup.find_all("ul",{"id":"gb-province"})
    li = ul[0].find_all("li")
    for i in li:
        citylst.append((i["data-procode"],i.text))
    return citylst
def gethtml(url):
    respnse = requests.post(url)
    respnse.encoding = respnse.apparent_encoding
    return respnse.text

def parsehtml(html,province):
    soup = BeautifulSoup(html,"html.parser")
    table = soup.find_all("table",{"id":"px"})
    thlst = table[0].find_all("tr")[1:]
    pagelst = []
    for tr in thlst:
        th = tr.find_all("th")
        onelst = [province,"2018","10"]
        for i in th[1:3]:
            onelst.append(i.text)
        pagelst.append(onelst)
    print(pagelst)
    file_csv(pagelst)

def file_csv(lst):
    file_size = os.path.getsize("inputData/houses.csv")
    if(file_size==0):
        name = ["province","year", "month", "city","price"]
        head_df = pd.DataFrame(columns=name, data=lst)
        head_df.to_csv("inputData/houses.csv", encoding="utf-8-sig", index=False)
    else:
        with open("inputData/houses.csv","a+",encoding="utf-8-sig",newline="") as file:
            wtiter = csv.writer(file)
            wtiter.writerows(lst)
def main():
    citylst = getCityLst()
    for i in citylst:
        if(i[1] not in ["北京","上海","重庆","天津","天津"]):
            parms = {"di":"all","pi":i[0],"ci":"","pt":11,"ty":"sale","un":"city","in":"Price","mn":"2018-10","ba1":"","ba2":"","br":"","bc":"","by1":"","by2":"","np1":"","np2":"","pr1":"","pr2":""}
            parms = str(parms).replace(" ","").replace("\'","\"")
            parmsencode = base64.b64encode(parms.encode("utf-8"))
            posturl = str(parmsencode)[2:-1] + ".html"
            url = "http://www.creprice.cn/rank/index/parms/"+posturl
            html = gethtml(url)
            parsehtml(html,i[1])
        # else:
        #     parms = {"di":"all","pi":i[0],"ci":"","pt":11,"ty":"sale","un":"district","in":"Price","mn":"2018-10","ba1":"","ba2":"","br":"","bc":"","by1":"","by2":"","np1":"","np2":"","pr1":"","pr2":""}
        #     parms = str(parms).replace(" ", "").replace("\'", "\"")
        #     parmsencode = base64.b64encode(parms.encode("utf-8"))
        #     posturl = str(parmsencode)[2:-1] + ".html"
        #     url = "http://www.creprice.cn/rank/index/parms/" + posturl

if __name__ == '__main__':
    main()