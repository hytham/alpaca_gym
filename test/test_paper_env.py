import gym
from configparser import ConfigParser
import envs

configur = ConfigParser()
conf = configur.read('config.ini')

env = gym.make('Alpaca_Paper-v0', config=conf['auth'])

Episodes = 1
obs = []
for _ in range(Episodes):
    observation = env.reset()
    done = False
    count = 0
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        obs = obs + [observation]
        count += 1
        if done:
            print(reward)
            print(count)
