FROM phusion/baseimage:latest

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH
ENV CONDA_DIR /opt/conda

WORKDIR /tmp

RUN apt-get update && apt-get install -y curl gcc \
    wget make g++ openssl libreadline-dev \
    libssl-dev libpcre3 libpcre3-dev \
    zlib1g zlib1g-dev gfortran \
    && wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p $CONDA_DIR \
    && export $CONDA_DIR/:$PATH \
    && conda config --set always_yes yes --set changeps1 no \
    && conda update -q conda \
    && conda info -a \
    && conda config --add channels intel \
    && conda create -q -n sse -c intel/label/test \
            python=3 r-base=3.4.1 pandas scikit-learn cython r-feather \
            libiconv r-survival r-dbi r-rmysql \
    && conda clean --all \
    && source activate sse \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-noconda.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && R --vanilla -e 'install.packages(c("survey","MonetDB.R"), repos="http://R-Forge.R-project.org")' \
    && mkdir -p /app

WORKDIR /app
COPY ./src /app/src
COPY ./config /app/config
COPY ./tests /app/tests


RUN pip install --no-cache-dir -e . \
    && apt-get purge --auto-remove -y gcc g++ make gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV MALLOC_MMAP_THRESHOLD_ 1000000
ENV MALLOC_MMAP_MAX_ 262144
ENV MALLOC_MXFAST_ 0

CMD survey_stats serve
