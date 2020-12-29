import numpy as np
import pandas as pd
import time

np.random.seed(2)
#全局变量
N_STATE = 6#总共的状态数
Actions = [0,1]#动作选择,0代表left，1代表right
EPOSION = 0.9#greedy
GAMA = 0.9#价值衰减率
ALPHA = 0.1#学习效率
MAX_EPISODES = 13
FRESH_TIME = 0.3#移动的时间


#建立Q表
def build_q_table(n_states,actions):
    table = pd.DataFrame(np.zeros((n_states,len(actions))),columns=actions)
    print(table)
    return table

#如何选择动作
def choose_action(state,q_table):
    state_actions = q_table.iloc[state,:]#此时生成一个Series对象
    if(np.random.uniform() > EPOSION) or (state_actions.all()==0):
        action_name = np.random.choice(Actions)
    else:
        action_name = state_actions.argmax()#生成一个最大值的索引
    return action_name

def get_env_feedback(S,A):
    if A == 1:
        if S == N_STATE -2:#到达宝藏处
            S_ = N_STATE - 1
            R = 1#R代表reward，表示奖励值
        else:#向右移动
            S_ = S + 1
            R = 0
    else:#向左移动
        R = 0
        if S == 0:#在开始处
            S_ = S
        else:
            S_ = S - 1
    return S_,R#返回下一个state和reward

#更新环境，这里对于强化学习的学习过程没有影响，只有呈现的作用
def update_env(S,episode,step_counter):#这里的step_counter是计算总共花了多少步到达了宝藏处
    env_list = ["-"]*(N_STATE-1) + ["T"]
    if(S==(N_STATE-1)):
        interaction = "Episode %s : total_steps = %s " % (episode+1,step_counter)
        print("\r{}".format(interaction),end="")
        time.sleep(2)
        print("\r")
    else:
        env_list[S] = "o"
        interaction = "".join(env_list)
        print("\r{}".format(interaction),end="")
        time.sleep(FRESH_TIME)

#主循环
def rl():
    #首先生成Q表
    q_table = build_q_table(N_STATE,Actions)
    for episode in range(MAX_EPISODES):
        step_count = 0
        S = 0
        is_terminated = False#是否结束
        update_env(S,episode,step_count)
        while not is_terminated:
            A = choose_action(S,q_table)
            S_,R = get_env_feedback(S,A)#采取动作并且得到下一状态和奖励（reward）
            q_predict = q_table.iloc[S,A]#q估计
            if S_ != (N_STATE -1):
                q_target = R + GAMA*q_table.iloc[S_,:].max()#Q现实
            else:
                q_target = R#Q现实
                is_terminated = True
            q_table.iloc[S,A] += ALPHA * (q_target - q_predict)
            S = S_

            update_env(S,episode,step_count+1)
            step_count += 1
    return q_table

if __name__ == '__main__':
   rl()


