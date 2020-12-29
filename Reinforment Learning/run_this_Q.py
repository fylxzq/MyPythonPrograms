from Maze_env import Maze
from RL_BrainNew import QLearningTable

def update():
    for episode in range(10):
        #初始的环境
        observation = env.reset()
        while True:
            env.render()

            action = RL.choose_action(str(observation))
            print(action)

            observation_,reward,done = env.step(action)

            RL.learn(str(observation),action,reward,str(observation_))

            observation = observation_

            if done:
                break
    print("game over")
    env.destroy()


if __name__ == '__main__':
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(10,update())
    print(RL.q_table.index)
    env.mainloop()