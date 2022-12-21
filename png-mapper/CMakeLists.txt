cmake_minimum_required(VERSION 3.22)
project(png_mapper_exe)

set(CMAKE_CXX_STANDARD 20)

add_executable(png_mapper_exe src/main.cpp src/Shape.cpp src/Shape.h src/bitmap_image.hpp src/CSVReader.cpp src/CSVReader.h)
