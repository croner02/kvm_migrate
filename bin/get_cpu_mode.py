import json
import sys

CPU_MODEL = [
    "SandyBridge",
    "IvyBridge",
    "Haswell",
    "Broadwell",
]

FILE_PATH = {
    "NOVA_PATH" : "/tmp/%s_nova.conf",
    "CPU_JSON_PATH" : "/tmp/%s_cpu.json",
}

def get_cpu():
    num = 0
    cpu_model = None
    with open('/proc/cpuinfo') as fd:
        for line in fd:
            if line.startswith('processor'):
                num += 1
            if line.startswith('model name'):
                cpu_model = line.split(':')[1].strip().split()
                cpu_model = cpu_model[-4] + ' ' + cpu_model[-3] + ' ' + cpu_model[-1]
    return {'cpu_num': num, 'cpu_model': cpu_model}


def create_cpu_json():
    cpu_info = get_cpu()
    with open(FILE_PATH["CPU_JSON_PATH"] % sys.argv[1], "wb") as f:
        json.dump(cpu_info, f)


if __name__ == "__main__":
    create_cpu_json()
