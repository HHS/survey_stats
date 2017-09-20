#!/bin/bash
# setup paths for install
export PATH="$HOME/miniconda/bin:$PATH"

setup_miniconda (){
    PLATF=`uname`
    # setup miniconda3
    # wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    apt-get update && \
    apt-get install -y curl gcc wget make g++ openssl libreadline-dev \
                       libssl-dev libpcre3 libpcre3-dev zlib1g zlib1g-dev \
                       gfortran
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -O miniconda.sh
    chmod +x miniconda.sh
    ./miniconda.sh -b -p $HOME/miniconda
}

install (){
    $COND = `which conda`
    if [ $COND -eq 0 ]; then
        echo "found miniconda at $COND, skipping the install..."
    else
        echo "couldn't find miniconda on the path, installing..."
        setup_miniconda
    fi

    CURDIR=`pwd`

    echo "update conda and add intel channel"
    conda update -q conda
    conda info -a

    echo "create conda env with intel python 3.6 and gnu r 3.4.1"
    conda create -p venv -c intel/label/test python=3.6 r-base=3.4.1 pandas scikit-learn cython r-feather libiconv r-survival r-dbi

    echo "activate the env and install package and dev requirements with pip"
    source activate $CURDIR/venv
    pip install -r requirements-dev.txt
    pip install -e .
}

if [ ! -f .develop.lock ]; then
    echo "setting up development environment..."
    install
    survey_stats
    if [ $? -eq 0 ]; then
        echo "environment ready!"
        touch .develop.lock
    fi
else
    echo "environment exists, getting it ready..."
    CURDIR=`pwd`
    export PATH="$HOME/miniconda/bin:$PATH"
    source activate "$CURDIR/venv"
    echo "environment ready!"
fi

export MALLOC_MMAP_THRESHOLD_=1000000
export MALLOC_MMAP_MAX_=262144
export MALLOC_MXFAST_=0

