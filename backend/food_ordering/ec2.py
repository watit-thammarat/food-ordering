import os
import requests


def is_ec2_linux():
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    if not is_ec2_linux():
        return None
    try:
        response = requests.get(
            'http://169.254.169.254/latest/meta-data/local-ipv4')
        return response.text
    except:
        return None
