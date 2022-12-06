#!/bin/bash

mkdir build images
cd build || exit
cmake ..
make
./png_mapper_exe