#!/bin/bash
source /home/howie/.local/bin/virtualenvwrapper.sh
workon plank-env
python ~/plankseconds/planktime.py
deactivate
