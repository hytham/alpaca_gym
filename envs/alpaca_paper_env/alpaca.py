import gym
import numpy as np
import datetime
import logging

from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.rest import TimeFrame, URL

from gym import spaces

logging.basicConfig(level=logging.INFO)

''' Simple alpaca environment useing paper trading '''


class AlpacaPaperEnv(gym.Env):
    ALPACA_KEY = 'PKC214N339W3NI6YKQAS'
    ALPACA_SECRET = 'kQRkSroM697t5kVeZMokM8jyavgTObBnWLBBrk6w'
    order_id =''
    def __init__(self, alpaca_info):
        super(AlpacaPaperEnv, self).__init__()
        self.alpac_info = alpaca_info
        api = REST(key_id=self.ALPACA_KEY, secret_key=self.ALPACA_SECRET, base_url='https://paper-api.alpaca.markets')
        account = api.get_account()
        self.action_space = spaces.Discrete(3)
        data = api.get_bars(alpaca_info['symbol'], TimeFrame.Hour, "2021-06-08", "2022-06-08",
                            adjustment='raw').df.sort_index(
            ascending=False)
        self.data = data
        self.observation_space = {
            "open": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32),
            "high": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32),
            "low": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32)
        }
        self.observation_shape = data.shape
        self.isdone = False
        self.api = api
        self.account = account
        self.info = {
            "start_balance": self._get_account_balance(),
            "current_balance": self._get_account_balance(),
            "gain": 0,
            "start_price": 0,
            "orderid": "",
            "status": account.status,
            "qt": 0,
            'order': None,
            'current_trade': ''
        }
        logging.info('Environment initialized')

    def step(self, action):
        logging.info("Step successful!")

        if action == 1:  # buy
            self._trade('buy')
        elif action == 2:  # sell
            self._trade('sell')

        observation = next(self._get_obs())
        self.renderone(observation)
        info = self._get_info()
        done = self.isdone
        reward = 0
        return observation, reward, done, info

    def reset(self):
        self.api.cancel_all_orders()
        self.api.close_all_positions()
        observation = next(self._get_obs())
        self.renderone(observation)
        info = self._get_info()
        self.info['current_trade'] = ''
        logging.info('Environment reset')

        return observation, info

    def render(self):
        print(self.data)

    def renderone(self, obs):
        print(obs)

    def _get_obs(self):
        for index, d in self.data.iterrows():
            yield d

    def _get_info(self):
        self.info['portfolio'] = self.api.list_positions()
        return self.info

    def _trade(self, _side):
        if self.info['current_trade'] == '':
            order = self.api.submit_order(
                symbol=self.alpac_info["symbol"],
                side=_side,
                type='market',
                qty=self.alpac_info["qt"],
                time_in_force='day'
            )
            self.info['current_trade'] = _side
            self.info['order'] = order
        else:
            self.api.close_position(self.info['symbol'],self.info['qt'])
            self.info['current_trade'] = ''
            self.isdone = True

    def _get_account_balance(self):
        return self.account.cash
