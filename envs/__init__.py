from gym.envs.registration import register

register(
    id='Alpaca-v0',
    entry_point='envs.alpaca_env.alpaca:AlpacaEnv'
)