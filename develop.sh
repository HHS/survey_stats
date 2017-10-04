#!/bin/bash -x
# setup paths for install

export MALLOC_MMAP_THRESHOLD_=1000000
export MALLOC_MMAP_MAX_=262144
export MALLOC_MXFAST_=0

export PATH="$HOME/miniconda/bin:$PATH"

CURDIR=`pwd`
VENV_NAME="survey_env"
CONDA_CHANS="intel intel/label/test"
R_PKGS="c('survey','MonetDB.R')"
R_REPO="http://r-forge.r-project.org"

COND=`which conda`
COND_EXISTS=$?

setup_miniconda (){
    PLATF=`uname`
    sudo apt-get update && \
    sudo apt-get install -y curl gcc wget make g++ openssl libreadline-dev \
        libssl-dev libpcre3-dev zlib1g-dev gfortran lzop liblzo2-dev httpie zsh && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -O miniconda.sh && \
    chmod +x miniconda.sh && \
    yes | ./miniconda.sh -b -p $HOME/miniconda
}

setup_venv () {

    echo "update conda" && \
    conda update -y -q conda && \
    conda info -a && \
    echo "create conda env with required R and Python deps" && \
    conda create -n ${VENV_NAME} -f conda_env.yml && \
    source activate ${VENV_NAME} && \
    echo "install required R packages" && \
    R --vanilla --slave -e "install.packages($R_PKGS, repos='$R_REPO')" && \
    echo "activate the env and install survey_stats in dev mode" && \
    pip install -e .
}

install (){

    if [ -e $COND ]; then
        echo "found conda at $COND, skipping the install..."
    else
        echo "couldn't find miniconda on the path, installing..."
        setup_miniconda
    fi

    setup_venv
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
    source activate ${VENV_NAME}
    echo "environment ready!"
fi
