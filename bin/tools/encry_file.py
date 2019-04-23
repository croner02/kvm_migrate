import base64
import json

def check_json(lines):
    try:
        json.loads(lines)
    except Exception:
        return False
    else:
        return True

class EncryFile(object):
    def __init__(self, cnf_org):
        self.cnf_org = cnf_org

    def encry(self):
        f_org = open(self.cnf_org, "r")
        content = f_org.read()
        content1 = content.encode(encoding="utf-8")
        content2 = base64.b64encode(content1)
        f_org.close()
        with open(self.cnf_org, "wb") as f_org:
            f_org.write(content2)

    def decode(self, line):
        decode_str = base64.b64decode(line)
        if check_json(decode_str):
            return decode_str
        else:
            return self.decode(decode_str)

    def __call__(self, *args, **kwargs):
        with open(self.cnf_org, "rb") as f:
            if not isinstance(f.read(), bytes):
                self.encry()
            f.seek(0, 0)
            json_info = self.decode(f.read())
        return json_info

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(EncryFile, "_instance"):
            EncryFile._instance = EncryFile(*args, **kwargs)
        return EncryFile._instance
