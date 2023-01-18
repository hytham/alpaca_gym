import unittest
import gym
import envs.alpaca_env

from configparser import ConfigParser


class AlpacaEnvTestCase(unittest.TestCase):
    def test_reset_test(self):
        configur = ConfigParser()
        configur.read('alpaca.test.ini')
        env = gym.make('Alpaca-v0', config=configur['auth'])
        observation = env.reset()
        self.assertEqual(True, len(observation[0][1]) > 0)  # add assertion here


if __name__ == '__main__':
    unittest.main()
