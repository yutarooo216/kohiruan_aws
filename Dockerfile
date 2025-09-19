FROM python:3.13

ARG pip_installer="https://bootstrap.pypa.io/get-pip.py"
ARG awscli_version="1.16.236"

# install command.
RUN apt-get update && apt-get install -y less vim jq unzip sshpass wget curl sudo

# create local bin directory
RUN mkdir -p /root/.local/bin
ENV PATH $PATH:/root/.local/bin

# install aws-cli ver2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# install ecr helper
RUN apt-get install -y amazon-ecr-credential-helper

# install sam
RUN pip install --user --upgrade aws-sam-cli

# install Terraform v1.5.7
RUN wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
RUN unzip terraform_1.5.7_linux_amd64.zip
RUN mv terraform /usr/local/bin/
RUN terraform version

RUN aws --version

RUN echo "alias ll='ls -al'" >> /root/.bashrc

# user add
RUN groupadd -g 1000 user
RUN useradd -m -s /bin/bash -u 1000 -g 1000 user1

# docker soket
RUN usermod -aG docker user1

USER user1
WORKDIR /home/user1

USER root
