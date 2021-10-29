from gym.envs.registration import register


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