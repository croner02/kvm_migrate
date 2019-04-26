# -*- coding: utf-8 -*-
from bin import parse_xml
from bin.log import logger


class ModifyXml(object):
    def __init__(self, src_xml, dest_xml):
        self.src_xml = src_xml
        self.dest_xml = dest_xml
        self.src_parse = parse_xml.ParseXml(self.src_xml)
        self.dest_parse = parse_xml.ParseXml(self.dest_xml)

    def modify_xml(self, key_path):
        dest_element_key = dict()
        src_element = self.src_parse.get_element(key_path)
        dest_element = self.dest_parse.get_element(key_path)
        element_tree = src_element["element_tree"]
        tree = src_element["tree"]
        if src_element["element_count"] != dest_element["element_count"]:
            if not ("host" in key_path):
                logger.error("%s must be equal" % key_path)
                raise Exception("%s must be equal" % key_path)
        for element_id, info in enumerate(dest_element["element"]):
            dest_element_key[element_id] = info
        try:
            i = 0
            for device in element_tree:
                for n in element_tree[i].attrib.keys():
                    name = n.strip()
                    device.set(name,  dest_element_key[i][name])
                    logger.debug("%s modify successfully" % key_path)
                i += 1
        except Exception, e:
            print e
        else:
            tree.write(self.src_xml, encoding="utf-8")

