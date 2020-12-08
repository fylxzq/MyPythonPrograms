import time
import turtle
import os
from turtle import *
from time import sleep

def draw_rectangle(start_x, start_y, rec_x, rec_y):
    turtle.goto(start_x, start_y)
    turtle.color('red')
    turtle.fillcolor('red')
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(rec_x)
        turtle.left(90)
        turtle.forward(rec_y)
        turtle.left(90)
    turtle.end_fill()
def draw_star(center_x, center_y, radius):
    turtle.setpos(center_x, center_y)
    # find the peak of the five-pointed star
    pt1 = turtle.pos()
    turtle.circle(-radius, 72)
    pt2 = turtle.pos()
    turtle.circle(-radius, 72)
    pt3 = turtle.pos()
    turtle.circle(-radius, 72)
    pt4 = turtle.pos()
    turtle.circle(-radius, 72)
    pt5 = turtle.pos()
    # draw the five-pointed star
    turtle.color('yellow', 'yellow')
    turtle.begin_fill()
    turtle.goto(pt3)
    turtle.goto(pt1)
    turtle.goto(pt4)
    turtle.goto(pt2)
    turtle.goto(pt5)
    turtle.end_fill()
def drawgap():
    penup()
    fd(2)
def drawdight(draw):
    drawgap()
    pendown() if draw else penup()
    fd(30)
    drawgap()
    right(90)
def drawhight(draw):
    drawgap()
    pendown() if draw else penup()
    fd(50)
    drawgap()
    right(90)
def draw(d):
    drawdight(True) if d in [2,3,4,5,6,8,9] else drawdight(False)
    drawdight(True) if d in [0,1,3,4,5,6,7,8,9] else drawdight(False)
    drawdight(True) if d in [0,2,3,5,6,8,9] else drawdight(False)
    drawdight(True) if d in [0,2,6,8,] else drawdight(False)
    left(90)
    drawdight(True) if d in [0,4,5,6,8,9] else drawdight(False)
    drawdight(True) if d in [0,2,3,5,6,7,8,9] else drawdight(False)
    drawdight(True) if d in [0,1,2,3,4,7,8,9] else drawdight(False)
    left(180)
    fd(20)
def draw1(d):
    drawhight(True) if d in [2,3,4,5,6,8,9] else drawhight(False)
    drawhight(True) if d in [0,1,3,4,5,6,7,8,9] else drawhight(False)
    drawhight(True) if d in [0,2,3,5,6,8,9] else drawhight(False)
    drawhight(True) if d in [0,2,6,8,] else drawhight(False)
    left(90)
    drawhight(True) if d in [0,4,5,6,8,9] else drawhight(False)
    drawhight(True) if d in [0,2,3,5,6,7,8,9] else drawhight(False)
    drawhight(True) if d in [0,1,2,3,4,7,8,9] else drawhight(False)
    left(180)
    fd(140)

def drawdate(date):
    speed(5)
    pencolor("red")
    for i in(date):
        if i=="-":
            write("年",font=("Arial", 15, "normal"))
            pencolor("green")
            fd(40)
        elif i=="=":
            write('月',font=("Arial", 15, "normal"))
            pencolor("blue")
            fd(40)
        elif i=="+":
            write('日',font=("Arial", 15, "normal"))
        else:
            if len(date)==3:
               draw1(int(i))
            else:
               draw(eval(i))
def main2():
    turtle.goto(60,300)
    #right(95)
    penup()
    pensize(5)
    drawdate("1949-10=01+")
    turtle.goto(-50,50)
    drawdate("2020-10=01+")
    turtle.goto(-160,-40)
    #drawdate("2016-10=23+")
    hideturtle()
time.sleep(5)
# start the project
turtle.speed(5)
turtle.penup()
# draw the rectangle
star_x = -820
star_y = -50
len_x = 660
len_y = 440
draw_rectangle(star_x, star_y, len_x, len_y)
# draw the big star
pice = 660 / 30
big_center_x = star_x + 5 * pice
big_center_y = star_y + len_y - pice * 5
turtle.goto(big_center_x, big_center_y)
turtle.left(90)
turtle.forward(pice * 3)
turtle.right(90)
draw_star(turtle.xcor(), turtle.ycor(), pice * 3)
# draw the small star
turtle.goto(star_x + 10 * pice, star_y + len_y - pice * 2)
turtle.left(turtle.towards(big_center_x, big_center_y) - turtle.heading())
turtle.forward(pice)
turtle.right(90)
draw_star(turtle.xcor(), turtle.ycor(), pice)
# draw the second star
turtle.goto(star_x + pice * 12, star_y + len_y - pice * 4)
turtle.left(turtle.towards(big_center_x, big_center_y) - turtle.heading())
turtle.forward(pice)
turtle.right(90)
draw_star(turtle.xcor(), turtle.ycor(), pice)
# draw the third
turtle.goto(star_x + pice * 12, star_y + len_y - 7 * pice)
turtle.left(turtle.towards(big_center_x, big_center_y) - turtle.heading())
turtle.forward(pice)
turtle.right(90)
draw_star(turtle.xcor(), turtle.ycor(), pice)
# draw the final
turtle.goto(star_x + pice * 10, star_y + len_y - 9 * pice)
turtle.left(turtle.towards(big_center_x, big_center_y) - turtle.heading())
turtle.forward(pice)
turtle.right(90)
draw_star(turtle.xcor(), turtle.ycor(), pice)
turtle.home()
main2()
def zheng(a,b):
   pencolor(b)
   write(a,font=("Arial",80,"normal"))
   speed(5)
   for i in range(4):
      fd(110)
      left(90)
y = -300
turtle.goto(-800, y)
zheng("祝","red")
turtle.goto(-600,y)
zheng("祖","orange")
turtle.goto(-400,y)
zheng("国","yellow")
turtle.goto(-200,y)
zheng("71","green")
turtle.goto(0,y)
zheng("岁","cyan")
turtle.goto(200,y)
zheng("生","blue")
turtle.goto(400,y)
zheng("日","purple")
turtle.goto(600,y)
zheng("快","red")
turtle.goto(800,y)
zheng("乐","yellow")
turtle.ht()
time.sleep(1000)
os._exit(1)