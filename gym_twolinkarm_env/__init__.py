from gym.envs.registration import register

__version__ = '0.0.7'

register(
    id="TwoLinkArmEnv-v0",
    entry_point="gym_twolinkarm_env.envs.normal:TwoLinkArmEnv",
)

register(
    id="TwoLinkArmEnv-v1",
    entry_point="gym_twolinkarm_env.envs.gravity:TwoLinkArmEnvWithGravity",
)

register(
    id="TwoLinkArmEnv-v2",
    entry_point="gym_twolinkarm_env.envs.gravity_bottom:TwoLinkArmEnvWithGravityToBottom",
)