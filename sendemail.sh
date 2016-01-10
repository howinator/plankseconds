#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
workon plank-env
python planktime.py
deactivate
