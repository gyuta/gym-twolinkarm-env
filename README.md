# gym-twolinkarm-env
![readme](https://user-images.githubusercontent.com/53563180/139202301-a0a82502-b09e-4ded-989f-44c0d75a1870.gif)
## Installation
```
pip install gym-twolinkarm-env
```

## Usage example
``` python
# coding: utf-8
import gym
import gym_twolinkarm_env

env = gym.make("TwoLinkArmEnv-v0")

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