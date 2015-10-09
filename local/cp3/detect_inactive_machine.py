    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年10月7日 下午9:33:21
# 说明：找出不活跃的机子

import argparse
import time
import sched
from scapy.all import sr, srp, IP, UDP, ICMP, TCP, ARP, Ether

RUN_FREQUENCY = 10

scheduler = sched.scheduler(time.time, time.sleep)

def detect_intertive_host(scan_host):
    # scan the network to find scan_hosts are live or die
    global scheduler
    scheduler
