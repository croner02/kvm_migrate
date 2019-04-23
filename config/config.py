from bin.tools import encry_file
import os
import json
user_cls = encry_file.EncryFile("%s/bin/tools/user_info.json" % os.getcwd())
USER_INFO_JSON = user_cls()
USER_INFO = json.loads(USER_INFO_JSON)

MIGRATE_LIST = [
    {"migrate_src": ["192.168.39.5", "instance-0000007e"],
     "migrate_dest": ["192.168.41.3", "instance-00000004"]
     },
]

FILE_PATH = {
    "NOVA_PATH": "/tmp/%s_nova.conf",
    "CPU_JSON_PATH": "/tmp/%s_cpu.json",
    "VM_XML_PATH": "/tmp/%s.xml",
    "OPENSTACK_ADMINRC": "/tmp/%s_admin-openrc",
}
