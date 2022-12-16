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