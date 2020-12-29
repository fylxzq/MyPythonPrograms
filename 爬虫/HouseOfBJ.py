import  requests
import re
from requests.exceptions import RequestException
import csv
import time
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
    except RequestException:
        return None

def parse_one_page(content):
    try:
        soup = BeautifulSoup(content,"html.parser")
        items = soup.find("div",class_ = re.compile("js-tips-list"))
        for div in items.find_all("div",class_ = re.compile("ershoufang-list")):
            yield {
                "Name":div.find("a",class_ = re.compile("js-title")).text,
                "Type":div.find("dd",class_ = re.compile("size")).contents[3].text,
                "Area":div.find("dd",class_ = re.compile("size")).contents[5].text,
                "Towards":div.find("dd",class_ = re.compile("size")).contents[9].text,
                "Floor": div.find("dd", class_=re.compile("size")).contents[13].text.replace("\n",""),
                "Decorate":div.find("dd",class_ = re.compile("size")).contents[17].text,
                "Adress":div.find("span",class_ = re.compile("area")).text.strip().replace(" ","").replace("\n",""),
                "TotalPrice":div.find("span",class_ = re.compile("js-price")).text + div.find("span",class_ = re.compile("yue")).text,
                "Price":div.find("div",class_ = re.compile("time")).text
            }
            if div["Name","Type","Area","Towards","Floor","Decorate","Adress","Tota;Price","Price"] == None:
                return  None
    except Exception:
        return None
def main():
    for i in range(1,2):
        url = "http://bj.ganji.com/fang5/o{}/".format(i)
        content = get_one_page(url)
        print("第{}页抓取完毕".format(i))
        for div in parse_one_page(content):
            print(div)
        with open("Data.csv","a",newline = "") as f:
            fieldname = ["Name","Type","Area","Towards","Floor","Decorate","Adress","TotalPrice","Price"]
            writer = csv.DictWriter(f,fieldnames=fieldname)
            if i==1:
                writer.writeheader()
            for item in parse_one_page(content):
                writer.writerow(item)
        time.sleep(3)
if __name__ == '__main__':
    main()
