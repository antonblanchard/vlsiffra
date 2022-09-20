#!/bin/bash -e

source venv/bin/activate

unittest-parallel
flake8
