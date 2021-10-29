# https://www.hahack.com/codes/cmake/
cmake_minimum_required(VERSION 3.5.1)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

# redis 3.0 start
get_filename_component(REDIS_ROOT "${CMAKE_CURRENT_SOURCE_DIR}" ABSOLUTE)
message(STATUS "Project root directory is: ${REDIS_ROOT}")
add_subdirectory(deps)
set(SRC_SERVER
        src/adlist.c src/ae.c src/anet.c src/dict.c src/redis.c src/sds.c src/zmalloc.c
        src/lzf_c.c src/lzf_d.c src/pqsort.c src/zipmap.c src/sha1.c src/ziplist.c
        src/release.c src/networking.c src/util.c src/object.c src/db.c
        src/replication.c src/rdb.c src/t_string.c src/t_list.c src/t_set.c
        src/t_zset.c src/t_hash.c src/config.c src/aof.c src/pubsub.c
        src/multi.c src/debug.c src/sort.c src/intset.c src/syncio.c
        src/cluster.c src/crc16.c src/endianconv.c src/slowlog.c src/scripting.c
        src/bio.c src/rio.c src/rand.c src/memtest.c src/crc64.c src/bitops.c
        src/sentinel.c src/notify.c src/setproctitle.c src/blocked.c src/hyperloglog.c
        )
set(EXECUTABLE_OUTPUT_PATH src)
link_directories(deps/linenoise/ deps/lua/src deps/hiredis)
add_executable(redis-server ${SRC_SERVER})
target_include_directories(redis-server
        PRIVATE ${REDIS_ROOT}/deps/linenoise
        PRIVATE ${REDIS_ROOT}/deps/hiredis
        PRIVATE ${REDIS_ROOT}/deps/lua/src
        )
target_link_libraries(redis-server
        PRIVATE pthread
        PRIVATE dl
        PRIVATE m
        PRIVATE lua
        PRIVATE linenoise
        PRIVATE hiredis
        )
# redis 3.0 end

# Database
aux_source_directory(cpp/Database Database)
add_executable(Database ${Database})

# main
aux_source_directory(cpp/main main)
add_executable(main ${main})

# redis
aux_source_directory(cpp/Redis MyRedis)
add_executable(MyRedis ${MyRedis})

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
