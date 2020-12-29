import csv
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
def gethtml(page):
    url = "http://g.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page={0}&searchWord=%E7%9A%84&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio"
    response = requests.get(url.format(page))
    response.encoding = response.apparent_encoding
    return response.text

def parsehtml(html):
    soup = BeautifulSoup(html,"html.parser")
    divs = soup.find_all("div",{"class":"ResultCont"})
    totalList = []
    for div in divs:
        theme = div.find("div",{"class":"title"}).find("a").text
        themeurl = div.find("div",{"class":"title"}).find("a").get("href")
        themeurl = "g.wanfangdata.com.cn/" + themeurl
        author = div.find("div",{"class":"ResultMoreinfo"}).find("a").text
        journal = div.find("div",{"class":"ResultMoreinfo"}).find_all("a")[-2].text
        jrurl = div.find("div",{"class":"ResultMoreinfo"}).find_all("a")[-2].get("href")
        jrurl = "g.wanfangdata.com.cn" + jrurl
        cites = div.find("div",{"class":"result_new_operaRight result_new_operaItem"}).find_all("a")[0].find("span").text
        year =div.find("div",{"class":"ResultMoreinfo"}).find_all("a")[-1].text[:4]
        downloads = div.find("div", {"class": "result_new_operaRight result_new_operaItem"}).find_all("a")[1].find("span").text
        oneList = [theme,themeurl,author,journal,jrurl,year,cites,downloads]
        totalList.append(oneList)
    file_to_csv(totalList)

def file_to_csv(lst):
    file_size = os.path.getsize("inputData/journal.csv")
    if(file_size==0):
        names = ["theme","themeurl","author","journal","jrurl","year","cites","downloads"]
        file_test = pd.DataFrame(columns=names,data=lst)
        file_test.to_csv("inputData/journal.csv",encoding="utf-8",index=False)
    else:
        with open("inputData/journal.csv","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)

def main():
    for i in range(50):
        content = gethtml(i)
        parsehtml(content)

if __name__ == '__main__':
    main()