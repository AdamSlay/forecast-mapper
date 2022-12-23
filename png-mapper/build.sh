#!/bin/bash

#git init
#git pull https://github.com/kost/httpexec.git
#cd httpexec
#go build httpexec.go
#./httpexec -listen png-mapper:8080 -verbose 5
nc -l 8877
cd /src || exit
mkdir build images
cd build || exit
cmake ..
make
./png_mapper_exe