#!/bin/bash

# inputs IP, pem file location
if [ $# -ne 2 ]; then
    echo 'Please enter your pem location and EC2 public DNS as ./deploy_to_prod.sh pem-full-file-location EC2-Public-IPv4-DNS'
    exit 0
fi

# zip repo into gz file
cd ..
rm -f yldtokenmonitor.gzip
zip -r yldtokenmonitor.gzip yld-token-cap/* yld-token-cap/.env

# Send zipped repo to EC2
chmod 400 $1
scp -i $1 yldtokenmonitor.gzip ubuntu@$2:~/.
cd yld-token-cap

# Send docker installation script to EC2
scp -i $1 ./deploy/install_docker.sh ubuntu@$2:~/.

# sh into EC2
ssh -i $1 ubuntu@$2