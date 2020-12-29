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

def parse_page(content):
    soup = BeautifulSoup(content,'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    rst_lst = []
    for tr in trs:
        tds = tr.find_all('td')
        team_name = tds[1].text
        game_time = tds[2].text
        game_rst = tds[3].text
        host_guest = tds[4].text
        rival = tds[5].text
        shot_rate = tds[6].text
        rebounds = tds[15].text
        assists = tds[18].text
        get_scores = tds[23].text
        one_lst = [team_name,game_time,game_rst,host_guest,rival,shot_rate,rebounds,assists,get_scores]
        rst_lst.append(one_lst)
    print(rst_lst)
    file_to_csv(rst_lst)

def file_to_csv(lst):
    if not os.path.exists('inputData/lakes_data.csv'):
        f = open('inputData/lakes_data.csv', 'w')
        f.close()

    file_size = os.path.getsize("inputData/lakes_data.csv")
    if (file_size == 0):
        name = ['team_name', 'game_time', 'game_rst', 'host_guest','rival', 'shot_rate', 'rebounds', 'assists','scores']
        file_test = pd.DataFrame(columns=name, data=lst)
        file_test.to_csv("inputData/lakes_data.csv", encoding="utf-8", index=False)
    else:
        with open("inputData/lakes_data.csv", "a+", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)


def main():
    for i in range(0,3):
        url = 'http://www.stat-nba.com/query_team.php?page='+str(i)+'&QueryType=game&order=1&crtcol=tm_out&Team_id=LAL&PageNum=30&Season0=2018&Season1=2019#label_show_result'
        print(url)
        content = get_page_codes(url)
        parse_page(content)

if __name__ == '__main__':
    main()