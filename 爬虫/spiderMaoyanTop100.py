import  requests
import re
import os,csv
import pandas as pd
from multiprocessing import Pool
def get_one_page(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) "
                            "AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/"
                            "49.0.2623.22 Safari/"
                            "537.36 SE 2.X MetaSr 1.0"}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    return response.text

def parse_one_page(html):
    pattern = re.compile('<i class="board-index board-index-\d+">(\d+)</i>.*?<p class="name"><a href="/films/.*?" title="(.*?)" data-act.*?'
                         '<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?'
                         '<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i>',re.S)
    rst = re.findall(pattern,html)
    lst = []
    for data in rst:
        index = data[0]
        title = data[1]
        actors = data[2].strip()[3:]
        firstTime = data[3][5:]
        ratescore = data[4]+data[5]
        lst_one = [index,title,actors,firstTime,ratescore]
        lst.append(lst_one)
    file_to_csv(lst)
def file_to_csv(lst):
    file_size = os.path.getsize("inputData/top100Maoyan.csv")
    if (file_size==0):
        name = ["排名","标题","主演","上映时间","评分"]
        file_test = pd.DataFrame(columns=name,data=lst)
        file_test.to_csv("inputData/top100Maoyan.csv",encoding="utf-8-sig",index=False)
    else:
        with open("inputData/top100Maoyan.csv","a+",encoding="utf-8-sig",newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lst)

def main(i):
    url = "http://maoyan.com/board/4?offset=" + str(i * 10)
    html = get_one_page(url)
    parse_one_page(html)
if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(10)])