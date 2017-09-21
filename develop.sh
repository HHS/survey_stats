#!/bin/bash
# setup paths for install

export MALLOC_MMAP_THRESHOLD_=1000000
export MALLOC_MMAP_MAX_=262144
export MALLOC_MXFAST_=0

export PATH="$HOME/miniconda/bin:$PATH"

CURDIR=`pwd`
VENV_DIR="venv"
CONDA_CHAN="intel/label/test"
CONDA_PYPKGS="pandas scikit-learn cython rpy2"
CONDA_RPKGS=" r-feather libiconv r-survival r-dbi"
CONDA_PYVER="python=3.6"
CONDA_RVER="r-base=3.4.1"
CONDA_LIST="$CONDA_PYVER $CONDA_RVER $CONDA_PYPKGS $CONDA_RPKGS"
R_PKGS="c('survey','MonetDB.R')"
R_REPO="http://r-forge.r-project.org"

COND=`which conda`

setup_miniconda (){
    PLATF=`uname`
    # setup miniconda3
    # wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    sudo apt-get update && \
    sudo apt-get install -y curl gcc wget make g++ openssl libreadline-dev \
        libssl-dev libpcre3-dev zlib1g-dev gfortran httpie zsh && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -O miniconda.sh && \
    chmod +x miniconda.sh && \
    yes | ./miniconda.sh -b -p $HOME/miniconda
}

setup_venv () {

    echo "update conda and add intel channel" && \
    conda update -y -q conda && \
    conda info -a && \
    echo "create conda env with intel python 3.6 and gnu r 3.4.1" && \
    conda create -y -p $VENV_DIR -c $CONDA_CHAN $CONDA_LIST && \ 
    echo "install required R packages" && \
    R --vanilla --slave -e "install.packages($R_PKGS, repos='$R_REPO')" && \
    echo "activate the env and install package and dev requirements with pip" && \
    source activate $CURDIR/$VENV_DIR && \
    pip install -r requirements-dev.txt && \
    pip install -e .

}

install (){

    if [ $COND -eq 0 ]; then
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
    source activate "$CURDIR/$VENV_DIR"
    echo "environment ready!"
fi
