#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
import sys

COLOR_RED = '\033[1;31m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN = '\033[1;36m'
COLOR_GRAN = '\033[1;37m'
COLOR_WHITE = '\033[1;38m'
COLOR_RESET = '\033[1;39m'


class ColordFormatter(logging.Formatter):
    """A colorfull Fromatter"""

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.LOG_COLORS = {
            "DEBUG": "% s",
            "INFO": COLOR_GREEN + "%s" + COLOR_RESET,
            "WARNING": COLOR_YELLOW + "%s" + COLOR_RESET,
            "ERROR": COLOR_RED + "%s" + COLOR_RESET,
            "CRITICAL": COLOR_RED + "%s" + COLOR_RESET,
            "EXCEPTION": COLOR_RED + "%s" + COLOR_RESET
        }

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return self.LOG_COLORS.get(level_name, "%s") % msg


class Log(object):
    def __init__(self, filename="/var/log/migrate.log", level="debug",
                 is_console=True, logger_namae="migrate_debug"):
        try:
            self._level = level
            self._filename = filename
            self._logger = logging.getLogger(logger_namae)
            if not len(self._logger.handlers):
                self._logger.setLevel(self.get_map_level(self._level))
                # debug log
                fmt = '[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
                datefmt = "%Y-%m-%d %H:%M:%S"
                formatter = logging.Formatter(fmt, datefmt)
                file_handler = RotatingFileHandler(self._filename, mode='a')
                file_handler.setLevel(self.get_map_level(self._level))
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)



                if is_console:
                    # normal info log
                    fmt = "[%(asctime)s] %(levelname)s %(message)s"
                    datefmt = "%H:%M:%S"
                    stream_handler = logging.StreamHandler(sys.stderr)
                    stream_handler.setLevel(logging.INFO)
                    console_formatter = ColordFormatter(fmt, datefmt)
                    stream_handler.setFormatter(console_formatter)
                    self._logger.addHandler(stream_handler)
        except Exception as e:
            print (e)

    def tolog(self):
        return self._logger

    def get_map_level(self, level="debug"):
        level = str(level).lower()
        if level == "debug":
            return logging.DEBUG
        if level == "info":
            return logging.INFO
        if level == "warn":
            return logging.WARN
        if level == "error":
            return logging.ERROR
        if level == "critical":
            return logging.CRITICAL


Log()
logger = logging.getLogger("migrate_debug")
