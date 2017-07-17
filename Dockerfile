FROM continuumio/anaconda3

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# System packages
RUN apt-get update && apt-get install -y curl gcc wget make g++ openssl libssl-dev libpcre3 libpcre3-dev zlib1g zlib1g-dev

RUN conda update -y conda \
  && conda install -y r cython r-feather r-functional \
  && R --vanilla -e 'install.packages("survey", repos="http://R-Forge.R-project.org")'

RUN mkdir -p /app
WORKDIR /app

EXPOSE 7777

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir cython

RUN apt-get install -y libreadline-dev

COPY . /app

RUN python setup.py develop

ENV MALLOC_MMAP_THRESHOLD_ 1000000
ENV MALLOC_MMAP_MAX_ 262144
ENV MALLOC_MXFAST_ 0
ENTRYPOINT ["survey_stats serve"]
