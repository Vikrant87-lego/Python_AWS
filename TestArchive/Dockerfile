FROM mcr.microsoft.com/devcontainers/python:3
RUN apt-get update && apt-get install --no-install-recommends -yq software-properties-common 

#Install saml2aws

RUN CURRENT_VERSION=$(curl -Ls https://api.github.com/repos/Versent/saml2aws/releases/latest | grep 'tag_name' | cut -d'v' -f2 | cut -d'"' -f1)
#CURRENT_VERSION="2.36.4"

RUN wget https://github.com/Versent/saml2aws/releases/download/v2.36.4/saml2aws_2.36.4_linux_amd64.tar.gz

RUN tar -xzvf saml2aws_2.36.4_linux_amd64.tar.gz

RUN mv saml2aws /usr/local/bin/

RUN chmod u+x /usr/local/bin/saml2aws
RUN saml2aws --version

# Install jdk
RUN apt install default-jre -y
RUN apt install default-jdk -y

# Install Python modules
RUN pip install boto3
RUN pip install requests
RUN pip install python-dotenv

# Install node
RUN apt-get install -y curl \
  && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && curl -L https://www.npmjs.com/install.sh | sh

# Add Yarn
#RUN npm install -g yarn

# Install TestMo CLI 
RUN npm install -g @testmo/testmo-cli
