from turtle import *
def drawsnake(rad,angle,len,neckrad):
    for i in range(len):
        circle(rad,angle)
        circle(-rad,angle)
    circle(rad,angle/2)
    fd(rad/2)
    circle(neckrad,180)
    fd(rad*2/3)
def main():
    setup(1300,800,0,0)
    pythonsize=30
    pensize(pythonsize)
    pencolor("blue")
    seth(-40)
    drawsnake(40,80,5,pythonsize/2)
main()