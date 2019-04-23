# -*- coding:utf-8 -*-
from config import config
from bin import parse_xml, modify_xml, migrate
from bin import compare_cpu, check_host
from bin.log import logger
import clear
MODIFY_INFO_LIST = [
    "disk/source",
    "disk/auth",
    "disk/secret",
    "disk/source/host",
    "interface/virtualport",
    "interface/virtualport/paramters"
    "interface/target",
    "console/source",
    "serial/source",
    "graphics",
    "graphics/listen"

]


def main():
    for host in config.MIGRATE_LIST:
        "check host ip ping"
        ping_ok, ping_failed = check_host.ping_test([host["migrate_src"][0], host["migrate_dest"][0]])
        if len(ping_failed) == 0:
            logger.debug(" ".join(ping_ok) + "ping reachable")
        else:
            logger.error(" ".join(ping_failed) + "ping unreachable")
        "compare host cpu model"
        cpu_compare_result = compare_cpu.compare_nova_conf(host["migrate_src"][0], host["migrate_dest"][0])
        if not cpu_compare_result:
            raise Exception("cpu model is Different, please modify nova_conf")
        """migrate xml modify"""
        xml_dic = parse_xml.GetVmXml(host["migrate_src"][0], host["migrate_dest"][0],
                                     host["migrate_src"][1], host["migrate_dest"][1])
        xml_dic = xml_dic.get_xml()
        src_xml_file = xml_dic["src_xml_file"]
        dest_xml_file = xml_dic["dest_xml_file"]
        modify_info = modify_xml.ModifyXml(src_xml_file, dest_xml_file)
        for info in MODIFY_INFO_LIST:
            modify_info.modify_xml(info)
        """migrate"""
        migrate_class = migrate.Migrate(host["migrate_src"][0], host["migrate_dest"][0],
                                        host["migrate_src"][1], host["migrate_dest"][1])
        migrate_class.start_vm()
        clear.clear()


if __name__ == "__main__":
    main()


