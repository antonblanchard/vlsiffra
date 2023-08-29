#!/bin/bash -e

python3 -m venv venv
source venv/bin/activate
python3 -c 'import sys; print("Python version:", sys.version)'
pip3 install .
pip3 install unittest-parallel
pip3 install flake8
pip3 install amaranth-yosys
