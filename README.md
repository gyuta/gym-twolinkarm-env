# gym-twolinkarm-env

## Installation
```
pip install gym-twolinkarm-env
```

## Usage example
``` python
# coding: utf-8
import gym
import gym_twolinkarm_env

env = gym.make("TwoLinkArm-v0")

for ep in range(10):
    env.reset()
    for step in range(200):
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)
        env.render()
```

## detail
# env
# state
# phisics
# reward
# action