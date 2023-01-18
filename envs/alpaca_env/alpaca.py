import logging
import gym
import numpy as np

from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import TimeFrame
from gym import spaces

logging.basicConfig(level=logging.INFO)

''' Simple alpaca environment using paper trading '''


class AlpacaEnv(gym.Env):
    actions = ['buy', 'sell', 'hold']

    def __init__(self, config):
        super(AlpacaEnv, self).__init__()
        api = REST(key_id=config['ALPACA_KEY'], secret_key=config['ALPACA_SECRET'], base_url=config['ALPACA_URL'])
        account = api.get_account()
        self.action_space = spaces.Discrete(len(self.actions))
        data = api.get_bars(config['TRADING_SYMBOL'], TimeFrame.Hour, "2021-06-08", "2022-06-08",
                            adjustment='raw').df.sort_index(
            ascending=False)
        self.data = data
        self.observation_space = {
            "open": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32),
            "high": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32),
            "low": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32),
            "close": spaces.Box(-1000.0, 1000.0, shape=(data.shape[0], 1), dtype=np.float32)
        }
        self.observation_shape = data.shape
        self.done = False
        self.api = api
        self.account = account
        self.info = {
            "symbol": config['TRADING_SYMBOL'],
            "start_balance": self._get_account_balance(),
            "current_balance": self._get_account_balance(),
            "gain": 0,
            "start_price": 0,
            "orderid": "",
            "status": account.status,
            "qt": config['QT'],
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
        done = self.done
        reward = 0
        return observation, reward, done, info

    def reset(self):
        self.api.cancel_all_orders()
        self.api.close_all_positions()
        observation = next(self._get_obs())
        info = self._get_info()
        self.info['current_trade'] = ''
        logging.info('Environment reset')

        return observation, info

    def render(self):
        print(self.data)

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
            self.order_id = order.id
        else:
            order_id = self.order_id
            self.api.cancel_order(order_id)
            self.info['current_trade'] = ''
            self.done = True

    def _get_account_balance(self):
        return self.account.cash
