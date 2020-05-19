import numpy as np


def itoa(msg):
    return np.array(list(msg.to_bytes(8, 'big')), np.int8)


def inttob(msg):
    return list(int(msg).to_bytes(8, 'big'))


def iptob(ip):
    return list(bytes(map(int, str(ip).split('.'))))


def mactob(mac):
    return list(bytes(map(lambda x: int(x, 16), str(mac).split(':'))))


def ltoa(lst):
    return np.array(lst, np.int8)
