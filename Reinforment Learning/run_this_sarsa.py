from Maze_env import Maze
from RL_BrainNew import SarsaTable

def update():
    for episode in range(10):
        #初始的环境
        observation = env.reset()

        action = RL.choose_action(str(observation))
        while True:
            #刷新环境
            env.render()
            #采取行动得到下一状态的observation 和 reward

            observation_,reward,done = env.step(action)
            #选择下一个环境的动作
            action_ = RL.choose_action(str(observation_))

            print(action_)

            observation_,reward,done = env.step(action)

            RL.learn(str(observation),action,reward,str(observation_),action_)

            observation = observation_
            action = action_

            if done:
                break
    print("game over")
    env.destroy()


if __name__ == '__main__':
    env = Maze()
    RL = SarsaTable(actions=list(range(env.n_actions)))

    env.after(100,update())
    env.mainloop()