import  requests
import re
def gethtml(url):
    referer = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&isinEn=1&dbPrefix=CJFQ&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%9c%9f%e5%88%8a%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=CJFQ.xml&research=off&t=1541645048301&keyValue=&S=1&sorttype=&DisplayMode=listmode"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"
    cookie =  "UM_distinctid=16362b38182134-0b41230d3392f7-6776a51-100200-16362b38183176; cnkiUserKey=e8061a51-69dd-4f7c-25da-086381dccb54; Ecp_ClientId=5180515152802715190; _pk_id=14bf67ee-3a41-442a-9936-36ecb14bad3b.1526369322.1.1526369557.1526369322.; RsPerPage=20; KNS_DisplayModel=listmode@CJFQ; CNZZDATA3258975=cnzz_eid%3D2147175785-1526366807-http%253A%252F%252Fxueshu.baidu.com%252F%26ntime%3D1541595127; Ecp_IpLoginFail=18110758.243.250.244; ASP.NET_SessionId=lgf4mopzgjkf3j0px1bppive; SID_kns=123120; SID_kinfo=125104; SID_klogin=125143; _pk_ref=%5B%22%22%2C%22%22%2C1541643768%2C%22http%3A%2F%2Fcnki.cyu.edu.cn%2F%22%5D; SID_krsnew=125131; _pk_ses=*; KNS_SortType=CJFQ%21%28%25e8%25a2%25ab%25e5%25bc%2595%25e9%25a2%2591%25e6%25ac%25a1%252c%2527INTEGER%2527%29+desc"
    header = {"User-Agent":user_agent,"Referer":referer,"Cookie":cookie}
    resonse = requests.get(url,headers=header)
    return resonse.text

def parsehtml(html):
    pattern = 'scrollbars=yes\',event\)">(.*?)</a>'
    rst = re.findall(pattern,html)
    return rst

def main():
    rst = []
    for i in range(1,6):
        url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage="+str(i)+"&RecordsPerPage=20&QueryID=7&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmodeRequest%20Method:GET&SortType=(被引频次%2c%27INTEGER%27)+desc&PageName=ASP.brief_result_aspx&isinEn=1#J_ORDER&"
        html =gethtml(url)
        feqlst = parsehtml(html)
        print(feqlst)
        rst.append(feqlst)
    return rst
def findH(rst):
    hlst = []
    for i in rst:
        a = rst.index(i)
        if(len(rst) - a > i):
            hlst.append(i)
    return hlst[-1]
if __name__ == '__main__':
    s = main()
    rst = []
    for i in s:
        rst += i
    for i in range(len(rst)):
        rst[i] = int(rst[i])
    sorted(rst)
    print("论文引用次数列表",rst)
    h = findH(rst)
    print("h指数是",h)


