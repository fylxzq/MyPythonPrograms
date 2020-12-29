import numpy as np
import pandas as pd

class RL(object):
    def __init__(self,action_spaces,learing_rate=0.1,reward_deacy = 0.9,e_greedy = 0.9):
        self.actions = action_spaces
        self.lr = learing_rate
        self.epislon = e_greedy
        self.gamma = reward_deacy
        self.q_table = pd.DataFrame(columns=self.actions,dtype=np.float64)

    def choose_action(self,observation):
        self.check_state_exists(observation)
        #选择行为

        if np.random.uniform() < 0.9:
            state_action = self.q_table.loc[observation,:]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action


    def check_state_exists(self,observation):
        if observation not in self.q_table.index:#不在Q表中，需要添加
            self.q_table =self.q_table.append(pd.Series([0]*len(self.actions),
                                              index=self.q_table.columns,
                                              name = observation))
    def learn(self,*args):#*args代表可选择的多参数
        pass

#离线学习
class QLearningTable(RL):
    def __init__(self,actions,learning_rate = 0.01,reward_deacy = 0.9,e_greedy=0.9):
        super(QLearningTable,self).__init__(actions,learning_rate,reward_deacy,e_greedy)

    #重写父类的learn方法
    def learn(self,s,a,r,s_):
        self.check_state_exists(s_)
        q_predict = self.q_table.loc[s,a]
        if s_ != "termianl":
            q_target = r + self.gamma * self.q_table.loc[s_,:].max()
        else:
            q_target = r
        self.q_table.loc[s,a] += self.lr *(q_target-q_predict)
#在线学习
class SarsaTable(RL):
    def __init__(self,actions,learing_rate = 0.1,reward_deacy=0.9,e_greedy=0.9):
        super(SarsaTable,self).__init__(actions,learing_rate,reward_deacy,e_greedy)

    def learn(self,s,a,r,s_,a_):
        self.check_state_exists(s_)
        q_predict = self.q_table.loc[s,a]
        if s_ != "terminal":
            q_target = r + self.gamma * self.q_table.loc[s_,a_]
        else:
            q_target = r
        self.q_table.loc[s,a] += self.lr * (q_target - q_predict)



