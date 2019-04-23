#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tools import shell_cmd
from config import config
from log import logger


def clear():
    for item in config.FILE_PATH.values():
        rm_cmd = "rm -rf " + item % "*"
        shell_cmd.shell_run(rm_cmd, exec_mode="localhost")
        logger.debug(item + "delete successfully!")
