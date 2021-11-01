#!/bin/sh

rm -f -r gym_twolinkarm_env.egg-info/* dist/*
python3 setup.py sdist bdist_wheel
twine upload --repository pypi dist/*