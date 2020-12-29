import pandas as pd
import numpy as np
import seaborn as sns
import  matplotlib as mltl
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
df = pd.read_csv("lianjia.csv")
df1 = df.copy()
df1["avgPrice"] = df["Price"] /df["Size"]
columns = ['Region', 'District', 'Garden', 'Layout', 'Floor', 'Year', 'Size', 'Elevator', 'Direction', 'Renovation', 'avgPrice', 'Price']
df = pd.DataFrame(df1,columns=columns)
df_house_count = df.groupby("Region")["Price"].count().sort_values(ascending=False).to_frame().reset_index()
df_house_mean = df.groupby("Region")["avgPrice"].mean().sort_values(ascending=False).to_frame().reset_index()
f,[ax1,ax2,ax3] = plt.subplots(3,1,figsize=(15,10))
sns.barplot(x="Region",y="avgPrice",palette="Blues_d",data=df_house_mean,ax=ax1)
ax1.set_title("北京各大区二手房每平方米单价对比",fontsize=15)
ax1.set_xlabel("区域")
ax1.set_ylabel("每平方米单价")

sns.barplot(x="Region",y="Price",palette="Reds_d",data=df_house_count,ax=ax2)
ax2.set_title("北京各大区二手房总数量对比",fontsize=15)
ax2.set_xlabel("区域")
ax2.set_ylabel("数量")

sns.boxplot(data=df,x="Region",y="Price")
ax3.set_title("北京各大区二手房房屋总价",fontsize=15)
ax3.set_xlabel("区域")
ax3.set_ylabel("房屋总价")
plt.show()
f,[ax1,ax2] = plt.subplots(1,2,figsize=(15,10))
sns.distplot(df["Size"],bins = 20,color="r",ax=ax1)
sns.kdeplot(df["Size"],ax=ax1,shade=True)
sns.regplot(x="Size",y="Price",ax=ax2,data=df)
plt.show()
df = df.loc[(df["Layout"] != "层拼别墅") & (df["Size"] < 1000)]
f,[ax1,ax2] = plt.subplots(1,2,figsize=(15,10))
sns.distplot(df["Size"],bins = 20,color="r",ax=ax1)
sns.kdeplot(df["Size"],ax=ax1,shade=True)
sns.regplot(x="Size",y="Price",ax=ax2,data=df)
plt.show()
