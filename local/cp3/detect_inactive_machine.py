    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月7日 下午9:33:21
# 说明：找出不活跃的机子，需安装scapy库，sudo pip install scapy
# 适用于局域网,某一网段的机子
# 未测试。

import argparse
import time
import sched
from scapy.all import sr, srp, IP, UDP, ICMP, TCP, ARP, Ether

RUN_FREQUENCY = 10

scheduler = sched.scheduler(time.time, time.sleep)

def detect_intertive_host(scan_host):
    # scan the network to find scan_hosts are live or die
    global scheduler
    scheduler.enter(RUN_FREQUENCY, 1, detect_intertive_host, (scan_host,))
    inactive_hosts = []
    try:
        ans, unans = sr(IP(dst = scan_host) / ICMP(), retry = 0, timeout = 1)
        ans.summary(lambda(s, r):r.sprintf("%IP.src% is alive"))
        for inactive in unans:
            print "%s is inactive" % inactive.dst
            inactive_hosts.append(inactive.dst)
        print "Total %d hosts are inactive " % (len(inactive_hosts))
    except KeyboardInterrupt:
        exit(0)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "python network utils")
    parser.add_argument('--scan-hosts', action = "store", dest = "scan_hosts", required = True)
    given_args = parser.parse_args()
    scan_hosts = given_args.scan_hosts
    scheduler.enter(1, 1, detect_intertive_host(scan_hosts,))
    scheduler.run()
