import  itchat
import  os
import time

sendmessage = "{消息助手}：暂时无法回复"
usemassage = "使用方法：\n1.运行CMD命令：cmd xxx (xxx为命令)\n" \
"-例如关机命令:\ncmd shutdown -s -t 0 \n" \
"2.获取当前电脑用户：cap\n3.启用消息助手(默认关闭)：ast\n" \
"4.关闭消息助手：astc"
flag = 0
nowtime = time.localtime()
print(nowtime)
filename = str(nowtime.tm_mday) + str(nowtime.tm_hour) + str(nowtime.tm_min) + str(nowtime.tm_sec) + ".txt"
myfile = open(filename,"w")
@itchat.msg_register("Text")
def text_reply(msg):
    global flag
    message = msg["Text"]
    fromname = msg["FromUserName"]
    toname = msg["ToUserName"]
    if toname == "fileheper":
        if message == "cap":
            itchat.send("告辞","filehelper")
        if message[0:3] == "cmd":
            os.system(message.strip(message[0:4]))
        if message == "ast":
            flag = 1
            itchat.send("消息助手已开启","filehelper")
        if message ==  "astc":
            flag = 0
            itchat.send("消息助手已关闭","filehelper")
    elif flag == 1:
        itchat.send(sendmessage,fromname)
        myfile.write(message)
        myfile.write("\n")
        myfile.flush()
if __name__ == '__main__':
    itchat.auto_login()
    itchat.send(usemassage, "filehelper")
    itchat.run()