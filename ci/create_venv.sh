#!/bin/bash -e

python3 -m venv venv
source venv/bin/activate
pip3 install .
pip3 install unittest-parallel
pip3 install flake8
pip3 install amaranth-yosys
