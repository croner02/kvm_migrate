#/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
from bin.log import logger

ping_ok = list()
ping_failed = list()
IP_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

class IPException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def check_ip_format(input_str):
    if isinstance(input_str, basestring):
        if re.match(IP_RE, input_str):
            return True if re.match(IP_RE,input_str) else False
    else:
        logger.error("Input format error, must be a string")
        raise IPException("Input format error, must be a string")


def ping_test(ip_list):
    global ping_ok
    global ping_failed
    for ip in ip_list:
        ping_cmd = "ping -c 2 -w 2 %s > /dev/null" % ip
        result = os.system(ping_cmd)
        if result == 0:
            ping_ok.append(ip)
        else:
            ping_failed.append(ip)
    return ping_ok, ping_failed

