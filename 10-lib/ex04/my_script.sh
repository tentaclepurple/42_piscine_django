#!/bin/bash

conda create -y -n django_venv python=3

source $(conda info --base)/etc/profile.d/conda.sh
conda activate django_venv

pip install -r requirement.txt


#source my_script.sh to keep the virtual env act
