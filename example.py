import gym
import gym_twolinkarm_env
import time

env = gym.make("TwoLinkArmEnv-v0")

for ep in range(10):
    env.reset()
    for step in range(50):
        time.sleep(0.1)
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)
        env.render()