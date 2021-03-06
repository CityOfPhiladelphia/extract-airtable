FROM ubuntu:16.04

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Define en_US.
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

RUN set -ex \
    && buildDeps=' \
        python3-dev \
        build-essential \
    ' \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        $buildDeps \
        python3 \
        python3-pip \
        locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && useradd -ms /bin/bash worker \ 
    && python3 -m pip install -U pip \
    && pip3 install -U setuptools

COPY extract_airtable /extract_airtable
COPY setup.py /setup.py
RUN set -ex \
    && pip3 install -e .

USER worker
#CMD ["/bin/bash"] 