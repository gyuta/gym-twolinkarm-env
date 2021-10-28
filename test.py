import gym
import twolinkarm

env = gym.make("TwoLinkArmEnv-v0")

for ep in range(10):
    env.reset()
    for step in range(200):
        env.render()
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)