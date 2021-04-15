#! /bin/bash

echo "Copying files.."
docker cp /home/andreo/Downloads/go1.16.3.linux-amd64.tar.gz fastdata:/
docker cp /media/sf_LubuntuVMfolder/gitTCC/lenses-cli-linux-amd64-4.2.0/lenses-cli-linux-amd64-4.2.0/lenses-cli fastdata:/usr/local/go/bin
## i will have to change those for git valid directories in the future
echo "Extracting.."
docker exec -i fastdata tar zxf go1.16.3.linux-amd64.tar.gz  -C /usr/local

echo "Setting environment variables.."
docker exec -i fastdata export PATH=$PATH:/usr/local/go/bin
docker exec -i fastdata export GO111MODULE=on
