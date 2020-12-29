import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
def gethtml(url):
    respnse = requests.get(url)
    respnse.encoding = respnse.apparent_encoding
    return respnse.text

def parshtml(html):
    soup = BeautifulSoup(html,"html.parser")
    print(type(soup))
    table = soup.find_all("table",{"class":"table_bg001 border_box limit_sale"})
    trs = table[0].find_all("tr")
    pagelst = []
    for tr in trs[1:]:
        onelst = []
        for td in tr.children:
            onelst.append(td.text)
        pagelst.append(onelst)
    file_csv(pagelst)


def file_csv(lst):
    file_size = os.path.getsize("inputData/stock.csv")
    if(file_size==0):
        name = ["datetime","startprice","maxprice","minprice","endprice","udamount",\
                "udrate","tradenum","tradeprice","rate","turnrate"]
        stock_df = pd.DataFrame(columns=name,data=lst)
        stock_df.to_csv("inputData/stock.csv",encoding="utf-8-sig",index=False)
    else:
        with open("inputData/stock.csv","a+",encoding="utf-8-sig",newline="") as flie:
            writer = csv.writer(flie)
            writer.writerows(lst)
def main():
    for i in range(2017,2019):
        for j in range(1,5):
            url = "http://quotes.money.163.com/trade/lsjysj_601939.html?year="+str(i)+"&season="+str(j)
            html = gethtml(url)
            parshtml(html)

if __name__ == '__main__':
    main()