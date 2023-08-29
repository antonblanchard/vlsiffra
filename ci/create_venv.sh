#!/bin/bash -e

python3 -m venv venv
source venv/bin/activate
python3 -c 'import sys; print("Python version:", sys.version)'

# Until amaranth 0.4 is published, Pythons newer than 3.9 need to install from git.
if [ "$(python3 -c 'import sys; print(sys.version_info[1])')" -gt 9 ]; then
	echo "Using Amaranth from GitHub as Python >3.9 (remove after Amaranth 0.4 is released)."
	pip3 install "git+https://github.com/amaranth-lang/amaranth.git#egg=amaranth"
fi

pip3 install .
pip3 install unittest-parallel
pip3 install flake8
pip3 install amaranth-yosys
