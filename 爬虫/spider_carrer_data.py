import requests
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
def get_page_codes(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    return resp.text
def get_player_data(player_id):#爬取球员数据的函数，参数是球员的id
    url = 'http://www.stat-nba.com/player/'+player_id+'.html'
    content = get_page_codes(url)
    soup = BeautifulSoup(content)#BeautifulSoup库解析页面
    rebunds = soup.find_all('td',{'class':'normal trb'})[0].text
    scores = soup.find_all('td',{'class':'normal pts'})[0].text
    assists = soup.find_all('td',{'class':'normal ast'})[0].text
    steals = soup.find_all('td',{'class':'normal stl'})[0].text
    shot_rate = soup.find_all('td',{'class':'normal fgper'})[0].text[:-1]
    block = soup.find_all('td',{'class':'normal blk'})[0].text
    rst = [scores, assists, rebunds, steals, shot_rate, block]
    print(rst)
    return rst
def parse_page(content):
    total_pleyers_datas = []
    soup = BeautifulSoup(content)
    pleyerlst_divs = soup.find_all('div',{'class':'playerList'})[1].find_all('div')
    for div in pleyerlst_divs:
        name_lst = div.find('span').text.split('/')
        chinese_name = name_lst[0].strip()
        english_name = name_lst[1].strip()
        href_str = div.find('a').get('href')#
        player_id = re.findall('player/(.*3?).html',href_str)[0]#获取球员的id
        player_career_data = get_player_data(player_id)#通过id拼接字符串爬取球员生涯的具体数据
        points = player_career_data[0]
        assists = player_career_data[1]
        rebunds = player_career_data[2]
        steals = player_career_data[3]
        shot_rate = player_career_data[4]
        block = player_career_data[5]
        one_lst = [chinese_name,english_name,points,assists,rebunds,steals,shot_rate,block]
        total_pleyers_datas.append(one_lst)
    file_to_csv(total_pleyers_datas)

def file_to_csv(lst):#将数据写入csv文件中
    if not os.path.exists('inputData/players_career_data.csv'):
        f = open('inputData/players_career_data.csv','w')
        f.close()

    file_size = os.path.getsize("inputData/players_career_data.csv")
    if (file_size==0):
        name = ['chinese_name','english_name','points','assists','rebounds','steals','shot_rate','block']
        file_test = pd.DataFrame(columns=name,data=lst)
        file_test.to_csv("inputData/players_career_data.csv",encoding="utf-8",index=False)
    else:
        with open("inputData/players_career_data","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)


def main():
    url = 'http://www.stat-nba.com/playerList.php'#
    content = get_page_codes(url)
    parse_page(content)

if __name__ == '__main__':
    main()