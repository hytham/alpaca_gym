import gym
import envs

env = gym.make('Alpaca_Paper-v0',alpaca_info = {
    'symbol':'AAPL',
    'start_date': '',
    'end_date': '',
})
obs,rew,d,info =env.step(1)
env.reset()


