import requests
from bs4 import BeautifulSoup#导入Beautiful Soup库解析页面
def gethtml(url):#获取文本函数
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    resp = requests.get(url,headers=headers)#设置请求头，应对简单的发爬虫
    resp.encoding = resp.apparent_encoding#设置编码
    return resp.text #返回response文本
def parse(text):#解析页面函数
    i = 1#相当于计数器
    soup = BeautifulSoup(text,'html.parser')
    rst = soup.find_all("li",{"class":"list-item"})#每条记录在li标签里
    print("编号","\t","简介","\t","户型","\t","大小","\t","楼层","\t","时间","\t","价格")
    for li in rst:#在li标签里找出需要的信息
        div = li.find("div",{"class":"house-details"})#
        title = div.find("div").find("a").text.strip().replace(" ",",")
        spans = div.find("div",{"class":"details-item"}).find_all("span")
        type = spans[0].text
        size = spans[1].text
        floors = spans[2].text
        date= spans[3].text
        price = li.find("span",{"class":"price-det"}).text
        print(i,"\t",title,"\t",type,"\t",size,"\t",floors,"\t",date,"\t",price)
        #打印输出
        i+=1#计数器加1
def main():#主函数
    url = "https://hf.anjuke.com/sale/a230-rd1/?bd_vid=11925466647022245258"
    text = gethtml(url)
    parse(text)

if __name__ == '__main__':
    main()