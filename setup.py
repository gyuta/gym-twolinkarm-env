import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gym-twolinkarm-env",
    version="0.1.1",
    author="gyuta",
    description="This is the open-ai-gym environment for controlling two link arm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gyuta/gym-twolinkarm-env",
    project_urls={
        "Bug Tracker": "https://github.com/gyuta/gym-twolinkarm-env/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "gym",
        "scipy",
        "pyglet"
    ],
    packages=["gym_twolinkarm_env", "gym_twolinkarm_env.envs"],
    package_data={
        "gym_twolinkarm_env": [
            "envs/assets/*.png"
        ]
    }
)