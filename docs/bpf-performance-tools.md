### BPF之巅

#### 参考资料
* [BPF之巅](https://book.douban.com/subject/35273652/)
* [bpftrace和Go语言](https://tonybai.com/2020/12/25/bpf-and-go-modern-forms-of-introspection-in-linux/)
* [BPF学习路径总结](https://www.ebpf.top/post/ebpf_learn_path/)
* [eBPF 与 Go 超能力组合](https://www.ebpf.top/post/ebpf_and_go/)
* IO Visor 项目开源的 BCC、 BPFTrace 和 Kubectl-Trace： 
  * BCC 提供了更高阶的抽象，可以让用户采用 Python、C++ 和 Lua 等高级语言快速开发 BPF 程序；
  * BPFTrace 采用类似于 awk 语言快速编写 eBPF 程序；
  * Kubectl-Trace 则提供了在 kubernetes 集群中使用 BPF 程序调试的方便操作；
* CloudFlare 公司开源的 eBPF Exporter 和 bpf-tools：
  * eBPF Exporter 将 eBPF 技术与监控 Prometheus 紧密结合起来；
  * bpf-tools 可用于网络问题分析和排查；
  
#### 纯C写的bpf程序
* [Write eBPF program in pure C](http://terenceli.github.io/%E6%8A%80%E6%9C%AF/2020/01/18/ebpf-in-c)

```
1，在ubuntu 22.04安装环境
apt-get install -y make clang llvm libelf-dev libbpf-dev bpfcc-tools libbpfcc-dev linux-tools-$(uname -r) linux-headers-$(uname -r)

2，把下面c程序贬义词bpf指令程序：clang -I/usr/src/linux-aws-headers-5.15.0-1022/include -O2 -c -target bpf -o mybpfobject.o mybpfcode.bpf.c
#include <uapi/linux/bpf.h>
#include "bpf/bpf_helpers.h"
int bpf_prog(void *ctx) {
    char buf[] = "Hello World!\n";
    bpf_trace_printk(buf, sizeof(buf));
    return 0;
}
（如果报错asm/types.h file not found则安装apt-get install -y gcc-multilib）

3，把bpf指令程序的纯指令提取出来：dd if=mybpfobject.o of=test_bpf bs=1 count=104 skip=64

4，用clang编译c程序：../bpf/test_bpf.c

5，运行a.out，它将捕获bpf的系统调用，如何查看：cat /sys/kernel/debug/tracing/trace_pipe
```

![img](../images/bpf/bpf_syscall.png)

#### BPF命令

![img](../images/bpf/bpf_command.jpg)

#### 辅助函数

![img](../images/bpf/bpf_helpers.jpg)

#### 映射类型

![img](../images/bpf/bpf_map_type.jpg)

#### 程序类型
* [06 | 事件触发：各类 eBPF 程序的触发机制及其应用场景](https://www.zadmei.com/sjcfglec.html)
* 全部类型：bpftool feature probe | grep program_type。可分为三类：
* 一，跟踪类，常用类型见[表格](../images/bpf/prog_type1.jpg)
* 二，网络类
  * XDP程序，常用类型见[表格](../images/bpf/prog_type2_xdp.jpg)
  * TC程序，类型有BPF_PROG_TYPE_SCHED_CLS、BPF_PROG_TYPE_SCHED_ACT
  * 套接字程序，常用类型见[表格](../images/bpf/prog_type2_socket.jpg)
  * cgroup程序，常用类型见[表格](../images/bpf/prog_type2_cgroup.jpg)
* 三，其他类，常用类型见[表格](../images/bpf/prog_type3.jpg)

#### 内核跟踪
```
// 如果/sys/kernel/debug目录不存在，执行
sudo mount -t debugfs debugfs /sys/kernel/debug

// 查看可kprobe跟踪的内核函数
cat /sys/kernel/debug/tracing/available_filter_functions | wc -l
bpftrace -l 'kprobe:*' | wc -l

// 查看tracepoint可跟踪的syscall函数
cat /sys/kernel/debug/tracing/available_events |grep syscalls:|wc -l
bpftrace -l 'tracepoint:syscalls:*' | wc -l

// 查看系统调用execeve的传参
cat /sys/kernel/debug/tracing/events/syscalls/sys_enter_execve/format // 不推荐
bpftrace -lv tracepoint:syscalls:sys_enter_execve

// 查看系统调用execeve的返回值
cat /sys/kernel/debug/tracing/events/syscalls/sys_exit_execve/format // 不推荐
bpftrace -lv tracepoint:syscalls:sys_exit_execve

开发BPF程序的三种方式：
bpftrace：依赖BCC
BCC：依赖LLVM和内核头文件
libbpf：要求内核>=5.2，并开启BTF特性(RHEL 8.2+和Ubuntu 20.10+)，是否有/sys/kernel/btf/vmlinux

// 查询调用execve的进程id和名称，以及传参argv
bpftrace -e 'tracepoint:syscalls:sys_enter_execve,tracepoint: { printf("%-6d %-8s", pid, comm); join(args->argv);}'
```

#### 如何开发一个负载均衡器
* [高性能网络实战（上）：如何开发一个负载均衡器？](https://www.zadmei.com/egxnwlsz.html)

```
// 将两个 eBPF 程序和映射加载到内核中，并固定到 BPF 文件系统中。
// 固定到 BPF 文件系统的好处是，即便 bpftool 命令已经执行结束，eBPF 程序还会继续在内核中运行。
bpftool prog load sockops.bpf.o /sys/fs/bpf/sockops type sockops pinmaps /sys/fs/bpf
bpftool prog load sockredir.bpf.o /sys/fs/bpf/sockredir type sk_msg map name sock_ops_map pinned /sys/fs/bpf/sock_ops_map

// 把 sockops 程序挂载到 cgroups
bpftool cgroup attach /sys/fs/cgroup/ sock_ops pinned /sys/fs/bpf/sockops
bpftool prog attach pinned /sys/fs/bpf/sockredir msg_verdict pinned /sys/fs/bpf/sock_ops_map

sockops 程序类型是 sock_ops；sockredir 程序类型是 sk_msg
sockops 挂载类型是 cgroup；  sockredir 挂载类型是 msg_verdict
```

#### 追踪go程序的调用栈

```
// 例如需要追踪net.Listen("tcp", ":6380")的调用栈，假设执行文件是test
// 下面的命令会显示net.socket的上游调用链，它的上游有net.Listen
bpftrace -e 'uprobe:./test:net.socket {printf("%s\n", ustack); }' -c ./test

// 如果调用栈只显示了内存地址，则可以用addr2line转换
bpftrace -e 'uprobe:./test:net.socket {printf("%s\n", ustack); }' -c ./test | addr2line -e ./test -f -p
```









