#!/usr/bin/env bash

rm -rf ./bulid/
rm -rf ./dist/
rm -rf ./optenum.egg-info/

echo "run 'python -m pip install --user --upgrade setuptools wheel' if error"
python setup.py sdist bdist_wheel
