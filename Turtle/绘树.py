from turtle import Turtle , mainloop
def tree(plist,l,a,f):
    if l>5:
        lst=[]
        print(plist)
        for p in plist:
            p.fd(l)
            q=p.clone()
            p.right(a)
            q.left(a)
            lst.append(p)
            lst.append(q)
        tree(lst,l*f,a,f)
def main():
    p=Turtle()
    p.color("green")
    p.pensize(5)
    p.speed(5)
    p.hideturtle()
    p.left(90)
    p.penup()
    p.goto(0,-200)
    p.pendown()
    tree([p],200,65,0.6375)
main()