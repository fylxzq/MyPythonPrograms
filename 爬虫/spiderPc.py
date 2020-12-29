import requests
from fake_useragent import UserAgent
import re

header = {"User-Agent":UserAgent(verify_ssl=False).random}
def gethtml(url):
    response = requests.get(url,headers=header)
    response.encoding = response.apparent_encoding
    return response.text

def parsehtml(html):
    pattern = re.compile('<img pic_type="0" class="BDE_Image".*?src="(.*?)"')
    picurl = re.findall(pattern,html)
    return picurl

def getpic(rst):
    for i in range(len(rst)):
        url = rst[i]
        pic = requests.get(url,headers=header)
        with open("inputData/pic/"+str(i)+".jpg","wb") as file:
            file.write(pic.content)
def main():
    url = "https://tieba.baidu.com/p/2460150866?pn=3"
    html = gethtml(url)
    picurl = parsehtml(html)
    getpic(picurl)


if __name__ == '__main__':
    main()