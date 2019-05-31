#!/usr/bin/env bash


echo "Install twine if missing. 'python -m pip install --user --upgrade twine'"

python -m twine upload dist/*