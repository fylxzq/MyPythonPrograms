import requests
import json
import pymysql
from xml import etree
#通过post请求获取json文件
def gethtml(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"\
              ,"Referer":"https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",\
              "Cookie":"_ga=GA1.2.1197149271.1548477306; user_trace_token=20190126123506-c15a7550-2123-11e9-a88f-525400f775ce; LGUID=20190126123506-c15a78a6-2123-11e9-a88f-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAGFABEF65CD19F85396BCD9894BD597F8376A81; _gat=1; _gid=GA1.2.204228817.1550922817; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548479496,1548751555,1548751568,1550922817; LGSID=20190223195339-a8b7a90f-3761-11e9-840c-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DkQnN1AqYNBosvP7T_GdYhR_2FPTsJ-1l61Gj37AGAJ3%26wd%3D%26eqid%3Deb59d6d0000e6049000000025c71343a; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=4f2bee5737bf4a8da21ded0e22b24c84; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550922824; LGRID=20190223195346-acda8cd4-3761-11e9-840c-5254005c3644; TG-TRACK-CODE=search_code"}
    data = {"first":"false","pn":2,"kd":"python"}
    resp = requests.post(url,data=data,headers=header)
    html = json.loads(resp.text)#json模块的loads函数，将已编码的 JSON 字符串解码为 Python 字典对象
    return html

#解析json
def parsejson(html):
    fullList = []
    positionList = html["content"]["positionResult"]["result"]
    for item in positionList:
        positionName = item["positionName"]
        workYear = item["workYear"]
        salary = item["salary"]
        city = item["city"]
        industryField = item["industryField"]
        companyFullName = item["companyFullName"]
        #positionLables = item["positionLables"]
        oneList = [positionName,workYear,salary,city,industryField,companyFullName]
        fullList.append(oneList)
    return fullList

def create_table():
    sql = "create table if not exists positions(positionName varchar(20) not null,\
        workYear varchar(20) not null,salary varchar(20) not null,city varchar(20) not null,industryField varchar(20) not null,\
        companyFullName varchar(20) not null,positionLables varchar(20) not null)"
    conn = pymysql.connect(host="localhost",port=3306,user="root",password="19980502",db="stu")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()

def insert_data(values):
    sql = "insert into positions values(%s,%s,%s,%s,%s,%s)"
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="19980502", db="stu")
    cursor = conn.cursor()
    cursor.executemany(sql,values)
    conn.commit()
    conn.close()

def getvalues(html):
    fuLLlsit = parsejson(html)
    values = []
    for item in fuLLlsit:
        value = (item[0],item[1],item[2],item[3],item[4],item[5])
        values.append(value)
    return values
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
def main():
    url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    html = gethtml(url)
    values = getvalues(html)
    print(values)
    #create_table()
    insert_data(values)
if __name__ == '__main__':
    main()