
"""
对于一些问题的注释
红色框 ：   探索者
黑色框 ：hell   陷阱       reward= -1
黄色框 ：paradise   终点       reward = 1
其他状态 :            reward = 0
"""

import numpy as np
import time
import tkinter as tk

UNIT = 40 #像素
MAZE_H = 4 #方框高度
MAZE_W = 4 #方框宽度

class Maze(tk.Tk,object):
    def __init__(self):#初始化函数
        super(Maze,self).__init__()#调用父类的函数
        self.action_space = ["U","D","L","R"]#移动一个有四种选择，上下左右
        self.n_actions = len(self.action_space)
        self.title("Maze")
        self.geometry("{0}x{1}".format(MAZE_H * UNIT,MAZE_W*UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self,bg="white",height=MAZE_H*UNIT,width = MAZE_W*UNIT)#构造画布
        #创建格子
        for c in range(0,MAZE_W * UNIT,UNIT):
            x0,y0,x1,y1 = c,0,c,MAZE_H * UNIT
            self.canvas.create_line(x0,y0,x1,y1)
        for r in range(0,MAZE_H *UNIT,UNIT):
            x0,y0,x1,y1 = 0,r,MAZE_W* UNIT,r
            self.canvas.create_line(x0,y0,x1,y1)

        #构造原始的表格
        origin = np.array([20,20])

        #陷阱1
        hell1_center = origin + np.array([UNIT*2,UNIT])
        self.hell1 = self.canvas.create_rectangle(hell1_center[0] - 15,
                                                  hell1_center[1] - 15,
                                                  hell1_center[0] + 15,
                                                  hell1_center[1] + 15,fill = "black")

        #陷阱2
        hell2_center = origin + np.array([UNIT,UNIT *2])
        self.hell2 = self.canvas.create_rectangle(hell2_center[0] - 15,
                                                  hell2_center[1] - 15,
                                                  hell2_center[0] + 15,
                                                  hell2_center[1] + 15,fill = "black")
        #创建宝藏
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(oval_center[0] - 15,
                                            oval_center[1] - 15,
                                            oval_center[0] + 15,
                                            oval_center[1] + 15,
                                            fill = "yellow")

        #创建红色框(移动的点)
        self.rect = self.canvas.create_rectangle(origin[0] - 15,
                                                 origin[1] - 15,
                                                 origin[0] + 15,
                                                 origin[1] + 15,
                                                 fill = "red")
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20,20])
        self.rect = self.canvas.create_rectangle(origin[0] -15,
                                                 origin[1] - 15,
                                                 origin[0] + 15,
                                                 origin[1] + 15,
                                                 fill = "red")
        #return observation
        #print(self.canvas.coords(self.rect))  输出结果：[5.0, 5.0, 35.0, 35.0]
        return self.canvas.coords(self.rect)

    def step(self,action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0,0])
        if action == 0:#向上
            if(s[1] > UNIT):
                base_action[1] -= UNIT
        elif action == 1:#向下
            if(s[1] < (MAZE_H -1 )*UNIT):
                base_action[1] += UNIT
        elif action == 2:#向右
            if s[0] < (MAZE_W-1)*UNIT:
                base_action[0] += UNIT
        elif action == 3:#向左
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect,base_action[0],base_action[1]) #Move Agent

        s_ = self.canvas.coords(self.rect) #下一个状态

        #奖励函数
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = "terminal"
        elif s_ in [self.canvas.coords(self.hell1),self.canvas.coords(self.hell2)]:
            reward = -1
            done = True
            s_ = "terminal"
        else:
            reward = 0
            done =False
        return  s_,reward,done

    def render(self):
        time.sleep(0.1)
        self.update()


if __name__ == '__main__':
    m = Maze()
    m.reset()
    m.mainloop()






