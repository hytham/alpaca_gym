import gym

from gym import spaces
''' Simple alpaca environment useing paper tradeing '''
class AlpacaPaperEnv(gym.Env):
    def __init__(self):
        super(AlpacaPaperEnv,self).__init__()
        self.action_space = spaces.Discrete(3,)
        print('Environment initialized')

    def step(self):
        print('Step successful!')

    def reset(self):
        print('Environment reset')

    def render(self):
        print('Environment reset')
