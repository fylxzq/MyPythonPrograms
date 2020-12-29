import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import re
import random
import time

def file_to_csv(lst):#将数据写入csv文件中
    if not os.path.exists('nba_races.csv'):
        f = open('nba_races.csv','w')
        f.close()

    file_size = os.path.getsize("nba_races.csv")
    if (file_size==0):
        name = ['game_time','hostteam','hostscore','hc_rate','hc_offs','hc_chapions','hpre_gap','visitteam','visitscore','vc_rate','vc_offs','vc_champions','vpre_gap']
        file_test = pd.DataFrame(columns=name,data=lst)
        file_test.to_csv("nba_races.csv",encoding="utf-8",index=False)
    else:
        with open("nba_races.csv","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)

def get_day_gaps(time1,time2):
    time1 = time.mktime(time.strptime(time1,'%Y-%m-%d'))
    time2 = time.mktime(time.strptime(time2,'%Y-%m-%d'))
    days = int((time1-time2)/(24*60*60))
    return days

def get_page_codes(url):
    # proxies = [{'http':'http://106.38.162.105:9000','https':'http://106.38.162.105:9000'}, \
    #            {'http': 'http://221.4.150.7:8181', 'https': 'http://221.4.150.7:8181'}]
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    return resp.text

def get_pre_gap(game_id,game_time):
    url = 'http://www.stat-nba.com/'+game_id
    codes = get_page_codes(url)
    soup = BeautifulSoup(codes,'html.parser')
    pre_time = soup.find('div', {'style': 'float: left;margin-top: 25px;margin-left: 10px;font-size: 16px;font-weight: bold;color: #009CFF'}).text.split()[0]
    gaps = get_day_gaps(game_time,pre_time)
    return gaps
def get_coach_info(coach_id):#获取教练信息的函数
    url = 'http://www.stat-nba.com' + coach_id
    content = get_page_codes(url)
    soup = BeautifulSoup(content, 'html.parser')
    coach_infos = str(soup.find_all('div',{'class':'detail'})[0])
    pattern = re.compile("支球队 (.*?)次进入.*?胜率(.*?)\%</div>.*?军:</div>(.*?)个",re.S)
    infos = re.findall(pattern,coach_infos)
    off_times = infos[0][0]
    wins_rate = infos[0][1]
    champions = infos[0][2]
    coach_info_lst = [off_times,wins_rate,champions]
    return coach_info_lst

def parse_page(content,rst):
    soup = BeautifulSoup(content,'html.parser')
    race_type = soup.find('div',{'class':'title'}).text[-4:-1]
    if(race_type=='常规赛'):
        game_time = soup.find('div',{'style':'float: left;margin-top: 25px;margin-left: 10px;font-size: 16px;font-weight: bold;color: #009CFF'}).text.split()[0]
        visitteam = soup.find_all('a',{'style':'font-size:14px;'})[0].text
        visitscore = soup.find_all('div',{'class':'score'})[0].text
        hostscore = soup.find_all('div',{'class':'score'})[1].text
        hostteam  = soup.find_all('a', {'style': 'font-size:14px;'})[1].text
        cid_divs = soup.find_all('div',{'style':'float:left;width:960px;text-align: right;font-size:12px;color:#009CFF'})
        vcid = cid_divs[0].find('a').get('href')
        hcid = cid_divs[1].find('a').get('href')
        [vc_offs,vc_rate,vc_champions] = get_coach_info(vcid)
        [hc_offs,hc_rate,hc_chapions] = get_coach_info(hcid)
        flag = re.findall('\(赛前战绩(.*?)\)</a>',str(content))
        vflag = flag[0].strip()
        hflag = flag[1].strip()
        if(vflag!='0胜0负'):
            vpre_gameid = re.findall('href=(.*?)><<前一场比赛',str(content))[0].replace("\"",'')
            vpre_gap = get_pre_gap(vpre_gameid,game_time)
        else:
            vpre_gap = 1
        if(hflag!='0胜0负'):
            hpre_gameid = re.findall('href=(.*?)><<前一场比赛',str(content))[1].replace("\"",'')
            hpre_gap = get_pre_gap(hpre_gameid,game_time)
        else:
            hpre_gap = 1
        onelst = [game_time,hostteam,hostscore,hc_rate,hc_offs,hc_chapions,hpre_gap,visitteam,visitscore,vc_rate,vc_offs,vc_champions,vpre_gap]
        print(onelst)
        rst.append(onelst)
    else:
        pass

def main():
    rst = []
    for i in range(43000,43830):
        url = 'http://www.stat-nba.com/game/'+str(i)+'.html'
        print(url)
        content = get_page_codes(url)
        if(len(content)<100):
            continue
        parse_page(content,rst)
    print(rst)
    file_to_csv(rst)



if __name__ == '__main__':
    main()