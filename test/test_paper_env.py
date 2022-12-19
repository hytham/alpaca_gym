import gym
import envs

env = gym.make('Alpaca_Paper-v0', alpaca_info={
    'symbol': 'AAPL',
    'start_date': '',
    'end_date': '',
    'qt': 1
})

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

obs, rew, d, info = env.step(1)
