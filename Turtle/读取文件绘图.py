import turtle
def main():
    turtle.title("开始绘图")
    turtle.setup(800,800,0,0)
    pen=turtle.Turtle()
    pen.color("red")
    pen.pensize(5)
    pen.speed(5)
    result=[]
    fh=open("D:/pycharm/程序/1.txt","r")
    for line in fh:
        result.append(list(map(float,line.split(","))))
    for i in range(len(result)):
        pen.color(result[i][3],result[i][4],result[i][5])
        pen.fd(result[i][0])
        if result[i][1]:
            pen.right(result[i][2])
        else:
            pen.left(result[i][2])
    pen.goto(0,0)
main()