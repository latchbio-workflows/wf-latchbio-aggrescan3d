# DO NOT CHANGE
FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:fe0b-main

WORKDIR /tmp/docker-build/work/

SHELL [ \
    "/usr/bin/env", "bash", \
    "-o", "errexit", \
    "-o", "pipefail", \
    "-o", "nounset", \
    "-o", "verbose", \
    "-o", "errtrace", \
    "-O", "inherit_errexit", \
    "-O", "shift_verbose", \
    "-c" \
]
ENV TZ='Etc/UTC'
ENV LANG='en_US.UTF-8'

ARG DEBIAN_FRONTEND=noninteractive

# Latch SDK
# DO NOT REMOVE
RUN pip install latch==2.53.3
RUN mkdir /opt/latch

# Install system requirements
RUN apt-get update --yes && \
    xargs apt-get install --yes gfortran aria2 git wget unzip curl && \
    apt-get install --fix-broken

# Install Mambaforge
RUN apt-get update --yes && \
    apt-get install --yes curl && \
    curl \
        --location \
        --fail \
        --remote-name \
        https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    `# Docs for -b and -p flags: https://docs.anaconda.com/anaconda/install/silent-mode/#linux-macos` \
    bash Mambaforge-Linux-x86_64.sh -b -p /opt/conda -u && \
    rm Mambaforge-Linux-x86_64.sh

# Set conda PATH
ENV PATH=/opt/conda/bin:$PATH

# Install Aggrescan3D
RUN conda create -n aggrescan3d_env python=2.7 pip -y

RUN conda run -n aggrescan3d_env conda install -c lcbio cabs -y && \
    conda run -n aggrescan3d_env conda install -c lcbio aggrescan3d -y

# Copy workflow data (use .dockerignore to skip files)
COPY . /root/

# Latch workflow registration metadata
# DO NOT CHANGE
ARG tag
# DO NOT CHANGE
ENV FLYTE_INTERNAL_IMAGE $tag

WORKDIR /root
