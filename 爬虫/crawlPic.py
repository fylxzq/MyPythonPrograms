import requests
import re
keyword = "情趣内衣"
header = {"UserAgent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
for i in range(0,1):
    url = "https://s.taobao.com/list?spm=a21bo.2017.201867-links-0.4.aa3d11d9I1lthv&q="+keyword+"&cat=16&seller_type=taobao&oetag=6745&source=qiangdiao&bcoffset=12&s="+str(i*60)
    response = requests.get(url,headers=header)
    response.encoding = response.apparent_encoding
    data = response.text
    pat = '"pic_url":"//(.*?)"'
    imgurlList = re.compile(pat).findall(data)
    for j in range(len(imgurlList)):
        print(j)
        imgurl = "http://" + imgurlList[j]
        img = requests.get(imgurl,headers=header)
        with open("C:/Users/de'l'l/Desktop/Python/图片/"+str(i)+str(j)+".jpg","wb") as file:
            file.write(img.content)
