import csv
import re,jieba
from wordcloud import WordCloud,ImageColorGenerator

import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
from os import path
import pandas as pd
mpl.rcParams['font.sans-serif'] = ['SimHei']
import numpy as np

time = []
nickName = []
gender = []
cityName = []
userLevel = []
score = []
content = ""

def read_csv():
    content =""
    with open("inputData/maoyan.csv","r",encoding="utf-8-sig",newline="") as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
                if i!=0:
                    time.append(row[0])
                    nickName.append(row[1])
                    gender.append(row[2])
                    cityName.append(row[3])
                    userLevel.append(row[4])
                    score.append(row[5])
                    content = content+row[6]
                i+=1
        print("一共有"+str(i)+"条记录")
        return content



def word_cloud(content):
    from pyecharts import WordCloud
    content = content.replace(" ",",")
    content = re.sub('[,，。. \r\n]',"",content)
    segment = jieba.lcut(content)
    words_df = pd.DataFrame({"segment":segment})
    stopwords = pd.read_csv("inputData/stopwords.txt",index_col=False,sep="\t",quoting=3,
                            names=["stopwords"],encoding="utf-8-sig")

    words_df = words_df[words_df.segment.apply(lambda x:False if x in list(stopwords.stopwords)+["电影"] else True)]
    words_stat = words_df.groupby(by=["segment"])["segment"].agg({"计数":np.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    test = words_stat.head(500).values
    codes = [test[i][0] for i in range(0,len(test))]
    counts = [test[i][1] for i in range(0,len(test))]
    wordcloud = WordCloud(width=1300,height=620)
    wordcloud.add("影评词云", codes, counts, word_size_range=[20, 100])
    wordcloud.render("c_wordcloud.html")

def jiebaText(text):
    word_lst = []
    text = re.sub('[,，。. \r\n]',"",text)
    seg_list = jieba.cut(text,cut_all=False)
    listStr = "-".join(seg_list)
    listStr = listStr.replace("class", "")
    listStr = listStr.replace("span", "")
    listStr = listStr.replace("悲伤逆流成河", "")
    with open("inputData/stopwords.txt",encoding="utf-8-sig") as file:
        stoplist = file.read()
    stoplist = stoplist.split("\n")
    for myword in listStr.split("-"):
        if (myword not  in stoplist) and (len(myword)>1):
            word_lst.append(myword)
        else:
            pass
    return "-".join(word_lst)

#评论词云图
def make_cloud(text1):
    text1 = text1.replace("悲伤逆流成河", "")
    bg = mpl.pyplot.imread("inputData/1.jpg")
    wc = WordCloud(
        background_color="white",
        width=890,
        height=600,
        mask=bg,
        max_font_size=150,
        random_state=50,
        font_path="c://simhei.ttf"
    ).generate_from_text(text1)
    bg_color = ImageColorGenerator(bg)
    plt.imshow(wc.recolor(color_func=bg_color))
    plt.axis("off")
    wc.to_file("word_cloud.png")

#评论者性别分布可视化
def sex_distribution(gender):
    list_num = []
    list_num.append(gender.count("0"))
    list_num.append(gender.count("1"))
    list_num.append(gender.count("2"))
    print(list_num)
    attr = ["其他","男","女"]
    fig,ax = plt.subplots(dpi=100,figsize=(5,5))
    ax.pie(list_num,labels=attr,startangle=90,autopct="%.f%%",pctdistance=0.3)
    ax.set_title("性别饼图")
    plt.show()

#评论者所在城市分布可视化
def city_distribution(cityName):
    city_dict = {}
    for i in cityName:
        if i in city_dict:
            city_dict[i] += 1
        else:
            city_dict[i] = 1
    sort_dict = sorted(city_dict.items(),key=lambda d:d[1],reverse=True)
    city_name = []
    people_num = []
    for i,j in sort_dict:
        city_name.append(i)
        people_num.append(j)
    import random
    from pyecharts import Bar
    bar = Bar("评论者城市分布")
    bar.add("", city_name, people_num, is_label_show=True, is_datazoom_show=True)
    bar.render("city_bar.html")
    # fig,ax = plt.subplots(figsize=(8,6),dpi=80)
    # ax.bar(np.arange(len(city_name)),people_num,width=0.5,tick_label=city_name)
    # ax.set_title("评论者城市分布")
    # ax.set_xlabel("城市")
    # ax.set_ylabel("人数")
    plt.show()

#每日评论可视化分析
def comment_visualization(time):
    from pyecharts import Line
    time_lst = list(set(time))
    time_dict = {}
    for i in range(len(time_lst)):
        time_dict[time_lst[i]] = time.count(time_lst[i])
    sort_lst = sorted(time_dict.items(),key=lambda d:d[0],reverse=False)
    time_name = []
    time_num = []
    for i,j in sort_lst:
        time_name.append(i)
        time_num.append(j)
    print(sort_lst)
    line = Line("评论数量日期折线图")
    line.add(
        "日期-评论数",
        time_name,
        time_num,
        is_fill=True,
        area_color="#000",
        area_opacity=0.3,
        is_smooth=True,
    )
    line.render("c_num_line.html")


def main():
    content = read_csv()
    # text = jiebaText(content)
    # make_cloud(text)
    #sex_distribution(gender)
    #city_distribution(cityName)
    comment_visualization(time)

if __name__ == '__main__':
    main()