FROM rocker/r-base

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# System packages
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda \
  && conda config --add channels intel \
  && conda create -n idp intelpython3_full python=3 \
  && R --vanilla -e 'install.packages("survey", repos="http://R-Forge.R-project.org")' \
  && R --vanilla -e 'install.packages("functional", repos="https://cloud.r-project.org/")' \
  && R --vanilla -e 'install.packages("feather", repos="https://cloud.r-project.org/")'

RUN mkdir -p /app
WORKDIR /app

EXPOSE 7777

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir cython

COPY . /app

RUN python3 setup.py develop

ENV MALLOC_MMAP_THRESHOLD_ 1000000
ENV MALLOC_MMAP_MAX_ 262144
ENV MALLOC_MXFAST_ 0
ENTRYPOINT ["survey_stats"]
