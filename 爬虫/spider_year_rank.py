import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import re
import random
import time

def get_page_codes(url):
    # proxies = [{'http':'http://106.38.162.105:9000','https':'http://106.38.162.105:9000'}, \
    #            {'http': 'http://221.4.150.7:8181', 'https': 'http://221.4.150.7:8181'}]
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    return resp.text

def get_coach_info(coach_id):#获取教练信息的函数
    url = 'http://www.stat-nba.com' + coach_id
    content = get_page_codes(url)
    soup = BeautifulSoup(content, 'html.parser')
    coach_infos = str(soup.find_all('div',{'class':'detail'})[0])
    pattern = re.compile("支球队 (.*?)次进入.*?胜率(.*?)\%</div>.*?军:</div>(.*?)个",re.S)
    infos = re.findall(pattern,coach_infos)
    print(infos)
    off_times = infos[0][0]
    wins_rate = infos[0][1]
    champions = infos[0][2]
    coach_info_lst = [off_times,wins_rate,champions]
    return coach_info_lst

def get_years(content):
    soup = BeautifulSoup(content,'html.parser')
    years = soup.find_all('div',{'style':'float: left;width: 870px;margin-left: 50px;margin-top: 2px;'})[0]
    years = re.findall('href="/wper/(\d+)\.html',str(years))
    return years

def file_to_csv(lst):#将数据写入文件
    if not os.path.exists('inputData/team_data1.csv'):
        f = open('inputData/team_data1.csv','w')
        f.close()

    file_size = os.path.getsize("inputData/team_data1.csv")
    if (file_size==0):
        name = ['year','team_name','wins','loss','win_rates','coach_off_times','coach_wins_rate','coach_champions']
        file_test = pd.DataFrame(columns=name,data=lst)
        file_test.to_csv("inputData/team_data1.csv",encoding="utf-8",index=False)
    else:
        with open("inputData/team_data1.csv","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)

def get_rank(content,year):#爬取球队每个赛季的战绩信息
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all('table')
    teams_info = []
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            team_name = tds[0].text
            wins = tds[1].text
            loss = tds[2].text
            win_rates = tds[3].text
            coach_id = tds[5].find('a').get('href')#得到球队教练的id
            infos = get_coach_info(coach_id)#获取教练的信息
            coach_off_times = infos[0]
            coach_wins_rate = infos[1]
            coach_champions = infos[2]
            team_info = [year,team_name,wins,loss,win_rates,coach_off_times,coach_wins_rate,coach_champions]
            teams_info.append(team_info)
    file_to_csv(teams_info)

def main():
    first_url = 'http://www.stat-nba.com/wper/1985.html'
    content = get_page_codes(first_url)
    years = get_years(content)#得到每个赛季的url连接
    for i in years:#循环遍历，爬取每个赛季球队的战绩
        time.sleep(2)
        url = 'http://www.stat-nba.com/wper/'+i+'.html'
        content = get_page_codes(url)
        get_rank(content,i)

if __name__ == '__main__':
    main()