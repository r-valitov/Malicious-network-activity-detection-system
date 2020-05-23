import numpy as np
import binascii


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


def unhexlify_array(arr):
    arr_bin = []
    for string in arr:
        arr_bin.append(int.from_bytes(binascii.unhexlify(string), 'big'))
    return arr_bin
