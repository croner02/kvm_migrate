from tools import shell_cmd
import json
from log import logger
import os
from config import config
import ConfigParser


def getremote_cpu_model(ip):
    put_scrit_args = "scp %s/bin/get_cpu_mode.py %s:/tmp/" % (os.getcwd(), ip)
    create_cpu_json_args = "python /tmp/get_cpu_mode.py %s " % ip
    shell_cmd.shell_run(put_scrit_args, exec_mode='localhost')
    shell_cmd.shell_run(create_cpu_json_args, host=ip, exec_mode='remote')
    logger.debug(config.FILE_PATH["CPU_JSON_PATH"] % ip + "create file successfully")


def getremote_nova_conf(ip):
    get_nova_args = "scp %s:/etc/nova/nova.conf %s "% (ip, config.FILE_PATH["NOVA_PATH"] % ip)
    shell_cmd.shell_run(get_nova_args, exec_mode="localhost")
    logger.debug(config.FILE_PATH["NOVA_PATH"] % ip + " create successfully ")


def compare_cpu_model(ip1, ip2):
    cpu_list = list()
    for ip in [ip1, ip2]:
        getremote_cpu_model(ip)
        file_path = config.FILE_PATH["CPU_JSON_PATH"] % ip
        args = "scp %s:/%s /tmp/" % (ip, file_path)
        shell_cmd.shell_run(args, exec_mode='localhost')
        with open(file_path, "r") as load_f:
            cpu_dict = json.load(load_f)
            cpu_list.append(cpu_dict)
    if cpu_list[0]["cpu_model"] == cpu_list[1]["cpu_model"]:
        logger.debug(cpu_list)
        return True, cpu_list
    else:
        logger.debug(cpu_list)
        return False, cpu_list


def compare_nova_conf(ip1, ip2):
    host_cpu_flag, host_cpu_model = compare_cpu_model(ip1, ip2)
    nova_dict = {}
    for ip in [ip1, ip2]:
        getremote_nova_conf(ip)
        conf = ConfigParser.ConfigParser()
        conf.read(config.FILE_PATH["NOVA_PATH"] % ip)
        cpu_mode = conf.get("libvirt", "cpu_mode")
        nova_dict[ip] = cpu_mode

    if host_cpu_flag:
        if nova_dict[ip1] == nova_dict[ip2]:
            logger.debug("host cpu model equal")
            return True
    else:
        if nova_dict[ip1] == nova_dict[ip2] and not nova_dict[ip1] == "host-passthrough":
            return True
        else:
            logger.debug(host_cpu_model)
            logger.error("cpu model is Different, please modify nova_conf")
            return False
