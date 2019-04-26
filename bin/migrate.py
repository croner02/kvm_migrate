#
# from tools import shell_cmd
#
# def migrate(src_host,dest_host, src_vm):
#     cmd_line= "virsh migrate --live --copy-storage-all --verbose " \
#               "--xml /tmp/%s.xml --dname %s_migrate %s " \
#               "qemu+tcp://%s/system" % (src_vm, src_vm, src_vm, dest_host)
#     mirrate_result=shell_cmd.run_cmd(cmd_line,src_host,exec_mode="remote", use_safe_shell=True)
#     return mirrate_result

from __future__ import print_function
import libvirt
import sys
import os
from novaclient import client as nova_client
from keystoneclient import session
from keystoneclient.auth.identity import v3 as v3_auth
from tools import shell_cmd
from config import config
from log import logger


class Migrate(object):

    def __init__(self, src_host, dest_host, src_vm, dest_vm):
        self.src_host = src_host
        self.src_vm = src_vm
        self.dest_host = dest_host
        self.dest_vm = dest_vm

    def migrate_init(self):
        self.src_conn = libvirt.open("qemu+tcp://%s/system" % self.src_host)
        self.dest_conn = libvirt.open("qemu+tcp://%s/system" % self.dest_host)
        dest_dom = self.dest_conn.lookupByName(self.dest_vm)
        dest_dom_status = True if dest_dom.isActive() == 1 else False
        if dest_dom_status:
            dest_dom.destroy()
        src_dom = self.src_conn.lookupByName(self.src_vm)
        return src_dom, dest_dom

    def migrate(self):
        xml_f = open(config.FILE_PATH["VM_XML_PATH"] % self.src_vm)
        xml = xml_f.read()
        xml_f.close()
        logger.info("migrate start.....%s To %s" % (self.src_vm, self.dest_host))
        src_dom, dest_dom = self.migrate_init()
        try:
            new_dom = src_dom.migrate2(self.dest_conn, xml,
                                       libvirt.VIR_MIGRATE_LIVE |
                                       libvirt.VIR_MIGRATE_NON_SHARED_DISK,
                                       "%s_migrate" % self.src_vm,
                                       uri="tcp://%s" % self.dest_host, bandwidth=0)
            if not new_dom:
                logger.error('Could not migrate to the new domain', file=sys.stderr)
        except Exception as e:
            exit(e)
            logger.error(e)
        logger.info('Domain was migrated successfully.')
        tmp_dom = self.dest_conn.lookupByName(self.src_vm + "_migrate")
        tmp_dom.destroy()
        logger.info("%s_migrate destroy successfully" % self.src_vm)
        dest_uuid = dest_dom.UUIDString()
        self.dest_conn.close()
        self.src_conn.close()
        return dest_uuid

    @staticmethod
    def create_adminrc(ip):
        files = config.FILE_PATH["OPENSTACK_ADMINRC"] % ip
        admin_cmd = "sshpass -p %s scp %s:/root/admin-openrc %s" % (config.USER_INFO["password"], ip,
                                                                    config.FILE_PATH["OPENSTACK_ADMINRC"] % ip)
        shell_cmd.shell_run(admin_cmd, ip, exec_mode='localhost')
        logger.debug("create %s successfully" % config.FILE_PATH["OPENSTACK_ADMINRC"] % ip)
        return files

    @staticmethod
    def get_adminrc(files):
        with open(files, 'r') as f:
            for line in f.readlines():
                if line.startswith("export"):
                    k, v = line.split("=")
                    k = k.strip("export ")
                    os.environ[k] = v.strip()

    def novaclient(self, ip):
        files = self.create_adminrc(ip)
        self.get_adminrc(files)
        client_kwargs = {
            "username": os.getenv("OS_USERNAME"),
            "password": os.getenv("OS_PASSWORD"),
            "auth_url": os.getenv("OS_AUTH_URL"),
            "user_domain_name": os.getenv("OS_USER_DOMAIN_NAME"),
            "project_name": os.getenv("OS_PROJECT_NAME"),
            "project_domain_name": os.getenv("OS_PROJECT_DOMAIN_NAME")
        }
        api_version = 2
        ks_session = session.Session(verify=True, cert=None)
        auth = v3_auth.Password(**client_kwargs)
        ks_session.auth = auth
        client = nova_client.Client(api_version, session=ks_session)
        return client

    def start_vm(self):
        nova = self.novaclient(self.dest_host)
        uuid = self.migrate()
        res = nova.servers.start(uuid)
        logger.info("%s target vm start successfuly !" % self.dest_vm)
        return res
