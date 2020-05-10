from environment.Envirnoment import Environment

env = Environment()
for i_episode in range(20):
    for t in range(100):
        action = env.action_space
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
