from subprocess import Popen, PIPE
import re
from typing import List, Dict
import socket
import struct


class ARP:
    def __init__(self, interface_ip: str, interface_num: int, ip: str, mac: str, is_dynamic: bool):
        self.interface_ip: str = interface_ip
        self.interface_num: int = interface_num
        self.ip: str = ip
        self.mac: str = mac
        self.is_dynamic = is_dynamic

    def __repr__(self):
        _t = "dynamic" if self.is_dynamic else "static"
        return f'if:{self.interface_ip},{hex(self.interface_num)} ip:{self.ip} mac:{self.mac} type:{_t}'

    def __str__(self):
        return self.__repr__()


def get_ip_mac() -> Dict[str, ARP]:
    def deal(_lines: List[str]) -> List[ARP]:
        _net_card = None
        _buf: List[ARP] = []
        for _l in _lines:
            _a = re.split(r'\s+', _l)
            if _a[0] == 'Interface:':
                _net_card = (_a[1], int(_a[3], 16))
            elif _a[0] == 'Internet':
                continue
            elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', _a[0]):
                _arp = ARP(_net_card[0], _net_card[1], _a[0], _a[1], _a[2] == 'dynamic')
                _buf.append(_arp)
        return _buf

    cmd = 'arp -a'
    proc = Popen(cmd, shell=True, stdout=PIPE)
    out: bytes = proc.stdout.read()
    lines = [line.strip() for line in out.decode().split('\n')
             if len(line.strip()) > 0]
    arps = deal(lines)
    return {x.ip: x for x in arps}


def ip2int(ip: str) -> int:
    return struct.unpack('>I', socket.inet_aton(ip))[0]


def int2ip(ip_int: int) -> str:
    return socket.inet_ntoa(struct.pack('>I', ip_int))
