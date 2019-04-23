import xml.etree.ElementTree as ET
from tools import shell_cmd
from bin.log import logger
from config import config
class CreateVmXml(object):
    def __init__(self, host, vm_name):
        self.host = host
        self.vm_name = vm_name
        self.args = "virsh dumpxml %s --inactive> %s " % (self.vm_name, config.FILE_PATH["VM_XML_PATH"] %self.vm_name)

    def create_xml(self, host):
        shell_cmd.shell_run(self.args, host, exec_mode="remote", use_safe_shell=True)
        logger.info(config.FILE_PATH["VM_XML_PATH"] %self.vm_name + " create successfully")

    def __call__(self, *args, **kwargs):
        return self.create_xml(host=self.host)


class GetVmXml(object):
    def __init__(self, src_host, dest_host, src_vm, dest_vm):
        self.src_host = src_host
        self.dest_host = dest_host
        self.src_vm = src_vm
        self.dest_vm = dest_vm

    def get_xml(self):
        # host_zip = dict(zip([self.src_host,self.dest_host],[self.src_vm,self.dest_vm]))
        CreateVmXml(host=self.src_host, vm_name=self.src_vm)()
        CreateVmXml(host=self.dest_host, vm_name=self.dest_vm)()
        # create_result=[CreateVmXml(host=h, vm_name=host_zip.get(h)) for h in host_zip.items()]
        return {
            "src_xml_file": config.FILE_PATH["VM_XML_PATH"] % self.src_vm,
            "dest_xml_file": config.FILE_PATH["VM_XML_PATH"] % self.dest_vm
        }


class ParseXml(object):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = self.read_xml()

    def read_xml(self):
        try:
            ET.register_namespace("nova", "http://openstack.org/xmlns/libvirt/nova/1.0")
            tree = ET.parse(self.xml_file)
        except IOError, e:
            tree = None
            logger.error("%s is error" % self.xml_file)
            logger.error(e)
        return tree

    def get_element(self, key_path):
        root = self.tree.getroot()
        element_list = [element for element in root[-1].findall(key_path)]
        element_attr = [element.attrib for element in element_list]
        return {
            "tree": self.tree,
            "element_tree": element_list,
            "element_count": len(element_list),
            "element": element_attr
        }
