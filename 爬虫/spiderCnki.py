import os
import time

import pandas
import requests
import csv
from bs4 import BeautifulSoup

def gethtml(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",\
              "Cookie":"Ecp_ClientId=8181208203302219582; RsPerPage=20; cnkiUserKey=31666fee-d63e-4b9e-768a-7576afbefe7c; Ecp_ClientIp=60.170.236.217; Hm_lvt_6e967eb120601ea41b9d312166416aa6=1577182473,1577238340; Ecp_session=1; ASP.NET_SessionId=0lhvq0v2bjg1ayilby3dv2tz; SID_kns=123124; SID_klogin=125142; SID_crrs=125133; SID_krsnew=125133; SID_kcms=124120; SID_kns_new=123121; SID_kinfo=125102; KNS_SortType=; DisplaySave=15; Ecp_IpLoginFail=19122658.243.250.186; _pk_ref=%5B%22%22%2C%22%22%2C1577358213%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*",\
              "Referer":"https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=1&dbPrefix=CFLS&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=on&t=1577358227263&keyValue=%E8%9A%81%E7%BE%A4&S=1&sorttype="}
    response = requests.get(url,headers=header,timeout=2)
    response.encoding = response.apparent_encoding
    return response.text

def parsrhtml(html):
    soup = BeautifulSoup(html,"html.parser")
    TRlst1 = soup.find_all("tr",{"bgcolor":"#ffffff"})
    TRlst2 = soup.find_all("tr",{"bgcolor":"#f6f7fb"})
    rst = []
    for tr in TRlst1:
        tdlst = tr.find_all("td")
        theme = tdlst[1].find("a").text
        author = tdlst[2].find("a").text
        university = tdlst[3].find("a").text
        degreee = tdlst[4].text.strip()
        year = tdlst[5].text.strip()
        cite = tdlst[6].find("span").find("a")
        if(cite!=None):
            cites=cite.text
        else:
            cites = 0
        downloads = tdlst[7].find("span").find("a").text
        one = [theme, author, university, degreee, year, cites, downloads]
        rst.append(one)
    for tr in TRlst2:
        tdlst = tr.find_all("td")
        theme = tdlst[1].find("a").text
        author = tdlst[2].find("a").text
        university = tdlst[3].find("a").text
        degreee = tdlst[4].text.strip()
        year = tdlst[5].text.strip()
        cite = tdlst[6].find("span").find("a")
        if (cite!=None):
            cites = cite.text
        else:
            cites = 0
        downloads = tdlst[7].find("span").find("a").text
        one = [theme,author,university,degreee,year,cites,downloads]
        rst.append(one)
    print(rst)
    file_csv(rst)

def file_csv(rst):
    file_size = os.path.getsize("inputData/degree.csv")
    if(file_size==0):
        name = ["theme","author","university","degree","year","cites","downloads"]
        essayInfo_df = pandas.DataFrame(columns=name,data=rst)
        essayInfo_df.to_csv("inputData/degree.csv",index=False,encoding="utf-8")
    else:
        with open("inputData/degree.csv","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rst)

def main():
        url = "https://kns.cnki.net/kns/brief/brief.aspx?curpage=2&RecordsPerPage=20&QueryID=3&ID=&turnpage=1&tpagemode=L&dbPrefix=CFLS&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&isinEn=1&"
        html = gethtml(url)
        print(html)
        parsrhtml(html)
        time.sleep(5)
if __name__ == '__main__':
    main()
