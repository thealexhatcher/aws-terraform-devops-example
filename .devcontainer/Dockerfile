FROM amazonlinux
## SYSTEM SETUP
RUN yum update -y
RUN yum install -y sudo gcc g++ make git zip unzip tar bzip2 wget jq openssl uuid aws-cli
## VSCODE USER Setup
RUN adduser vscode 
RUN usermod -aG wheel vscode
RUN echo '%vscode ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER vscode