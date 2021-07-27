# https://www.hahack.com/codes/cmake/
cmake_minimum_required(VERSION 3.5.1)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

# 创建型
aux_source_directory(cpp/SimpleFactory SimpleFactory)
add_executable(SimpleFactory ${SimpleFactory})

aux_source_directory(cpp/FactoryMethod FactoryMethod)
add_executable(FactoryMethod ${FactoryMethod})

aux_source_directory(cpp/AbstractFactory AbstractFactory)
add_executable(AbstractFactory ${AbstractFactory})

aux_source_directory(cpp/Singleton Singleton)
add_executable(Singleton ${Singleton})

# 结构型
aux_source_directory(cpp/Adapter Adapter)
add_executable(Adapter ${Adapter})

aux_source_directory(cpp/Decorator Decorator)
add_executable(Decorator ${Decorator})

aux_source_directory(cpp/Facade Facade)
add_executable(Facade ${Facade})

aux_source_directory(cpp/Proxy Proxy)
add_executable(Proxy ${Proxy})

# 行为型
# 命令模式：客户端只需要知道电视和Invoker（打开、关闭、换台），Invoker执行具体的Command，Command再对接电视
aux_source_directory(cpp/Command Command)
add_executable(Command ${Command})

aux_source_directory(cpp/Observer Observer)
add_executable(Observer ${Observer})

# 状态模式，TCPConnection包含三种状态TCPStat（TCPListen、TCPClosed、TCPEstablished），任意时刻只能处于一种状态
aux_source_directory(cpp/State State)
add_executable(State ${State})

aux_source_directory(cpp/Strategy Strategy)
add_executable(Strategy ${Strategy})
