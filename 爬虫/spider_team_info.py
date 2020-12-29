
import requests
from bs4 import BeautifulSoup

import re
def get_page_codes(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)
    resp.encoding = resp.apparent_encoding
    return resp.text

def get_team_info(team_Abb):
    lst = []
    url = 'http://www.stat-nba.com/team/'+team_Abb+'.html'
    content = get_page_codes(url)
    soup = BeautifulSoup(content, 'html.parser')
    team_name = re.findall('<title>(.*?)\|数据',content)[0]
    shot_rate = soup.find_all('td',{'class':'fgper'})[-2:][0].text[:-1]
    three_rate = soup.find_all('td',{'class':'threepper'})[-2:][0].text[:-1]
    push_rate = soup.find_all('td', {'class': 'ftper'})[-2:][0].text[:-1]
    ORB = soup.find_all('td',{'class','orb'})[-2:][0].text
    DRB = soup.find_all('td',{'class','drb'})[-2:][0].text
    AST = soup.find_all('td',{'class','ast'})[-2:][0].text
    BOK = soup.find_all('td',{'class','blk'})[-2:][0].text
    STL = soup.find_all('td', {'class','stl'})[-2:][0].text
    TOV = soup.find_all('td',{'class','tov'})[-2:][0].text
    Get_score = soup.find_all('td',{'class','pts'})[-2:][0].text
    Loss_score = soup.find_all('td',{'class','pts'})[-2:][1].text
    onelst = [team_name,shot_rate,three_rate,push_rate,ORB,DRB,AST,BOK,STL,TOV,Get_score,Loss_score]
    for i in onelst:
        print(i,end=',')
    print()


def get_team_Name(content):
    soup = BeautifulSoup(content,'html.parser')
    team_name = soup.find_all('a',{'class':'team'})
    team_lst = []
    for a in team_name[0:30]:
        print(a.text)
        team_Abb = a.get('href')[-8:-5]
        team_lst.append(team_Abb)
    return team_lst

def main():
    url = 'http://www.stat-nba.com/teamList.php'
    content = get_page_codes(url)
    team_lst = get_team_Name(content)
    for i in team_lst:
        get_team_info(i)

if __name__ == '__main__':
    main()