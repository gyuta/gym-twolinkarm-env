from gym.envs.registration import register


register(
    id="TwoLinkArmEnv-v0",
    entry_point="twolinkarm.envs.normal.TwoLinkArmEnv",
)

register(
    id="TwoLinkArmEnv-v1",
    entry_point="twolinkarm.envs.gravity.TwoLinkArmEnvWithGravity",
)