# https://www.hahack.com/codes/cmake/
cmake_minimum_required(VERSION 3.5.1)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

aux_source_directory(cpp/Adapter Adapter)
add_executable(Adapter ${Adapter})

aux_source_directory(cpp/SimpleFactory SimpleFactory)
add_executable(SimpleFactory ${SimpleFactory})

aux_source_directory(cpp/FactoryMethod FactoryMethod)
add_executable(FactoryMethod ${FactoryMethod})

aux_source_directory(cpp/AbstractFactory AbstractFactory)
add_executable(AbstractFactory ${AbstractFactory})