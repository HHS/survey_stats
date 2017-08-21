#!/bin/bash

# setup miniconda3
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
chmod +x miniconda.sh
./miniconda.sh -b -p $HOME/miniconda

# setup paths for install
export PATH="$HOME/miniconda/bin:$PATH"
hash -r

# update conda and add intel channel
conda update -q conda
conda info -a
conda config --add channels intel

# create conda env with intel python 3.6 and gnu r 3.4.1
conda create -q -n ssdev-intelpy36gnur34 -c intel/label/test python=3 r-base=3.4.1 pandas scikit-learn cython r-feather libiconv r-survival r-dbi

# activate the env and install package and dev requirements with pip
source activate ssdev-intelpy36gnur34
pip install -r requirements-dev.txt
pip install -e .

