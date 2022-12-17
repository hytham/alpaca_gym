from gym.envs.registration import register

register(
    id='Alpaca_Paper-v0',
    entry_point='envs.alpaca_paper_env.alpaca:AlpacaPaperEnv'
)