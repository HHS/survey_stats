FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y \
	python3 \
	python3-pip \
	python3-dev \
	build-essential \
	curl \
	gcc \
	wget \
	make \
	g++ \
	openssl \
	libreadline-dev \
	libssl-dev \
	libpcre3-dev \
	zlib1g-dev \
	gfortran \
	lzop \
	liblzo2-dev \
	httpie \
	zsh \
	vim

RUN mkdir -p /opt/statserver/
WORKDIR /opt/statserver/
ADD * ./

RUN echo "INSTALLING miniconda3"


RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
RUN chmod +x miniconda.sh
RUN ./miniconda.sh -b -p /opt/miniconda3

#Add conda to ENV and PATH for debug
ENV conda=/opt/miniconda3/bin/conda
RUN echo "PATH=$PATH:/opt/miniconda3/bin/" >> ~/.bashrc


RUN echo "RUNNING develop.sh"

RUN mkdir -p /var/log/statserver
RUN chmod +x develop.sh
RUN ./develop.sh > /var/log/statserver/develop.log