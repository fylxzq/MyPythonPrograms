import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
def get_page_codes(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    return resp.text

def file_to_csv(lst):
    if not os.path.exists('inputData/player_data.csv'):
        f = open('inputData/player_data.csv','w')
        f.close()

    file_size = os.path.getsize("inputData/player_data.csv")
    if (file_size==0):
        name = ['player_name','season','race_rst','rival','rate_shot','rebounds','assists','steals','caps','scores']
        file_test = pd.DataFrame(columns=name,data=lst)
        file_test.to_csv("inputData/player_data.csv",encoding="utf-8",index=False)
    else:
        with open("inputData/player_data.csv","a+",encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)
def parse_page(content):
    soup = BeautifulSoup(content,'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    rst_lst = []
    for tr in trs:
        tds = tr.find_all('td')
        player_name = tds[1].text
        season = tds[2].text
        race_rst = tds[3].text
        rival = tds[4].text
        rate_shot = tds[7].text
        rebounds = tds[16].text
        assists = tds[19].text
        steals = tds[20].text
        caps = tds[21].text
        scores = tds[24].text
        one_record = (player_name,season,race_rst,rival,rate_shot,rebounds,assists,steals,caps,scores)
        rst_lst.append(one_record)
    return rst_lst

def main():
    for i in range(60):
        url = 'http://www.stat-nba.com/query.php?page='+str(i)+'&crtcol=season&order=0&QueryType=game&GameType=season&Player_id=1862#label_show_result'
        content = get_page_codes(url)
        rst = parse_page(content)
        file_to_csv(rst)

if __name__ == '__main__':
    main()