import numpy as np
import pandas as pd

class QLearningTable:
    #初始化函数，初始化变量
    def __init__(self,actions,learing_rate=0.01,reward_decay=0.9,e_greedy=0.9):
        self.actions = actions
        self.lr = learing_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions,dtype=np.float64)

    def choose_action(self,observation):
        self.check_state_exist(observation)#检查状态是否存在,如果不存在则添加，否则啥都不做
        if np.random.uniform() < self.epsilon:
            #选择最好的行为
            state_action = self.q_table.loc[observation,:]
            #一些行为可能有相同的值，在这些行动中随机选取一个值
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            #随机选择行为
            action = np.random.choice(self.actions)
        return action

    def learn(self,s,a,r,s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s,a]
        if s_ != "terminal":#下一个状态不是终止状态
            q_target = r + self.gamma * self.q_table.loc[s_,:].max()
        else:
            q_target = r
        self.q_table.loc[s,a] += self.lr * (q_target - q_predict)#更新



    def check_state_exist(self,state):
        if state not in self.q_table.index:
            #添加新的状态到Q表中
            self.q_table = self.q_table.append(pd.Series([0]*len(self.actions),
                                               index = self.q_table.columns,name=state))





