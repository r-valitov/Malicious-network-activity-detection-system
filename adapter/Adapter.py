import pyshark

from utils.Misc import mactob, iptob, inttob, ltoa


class Adapter:
    def __init__(self):
        self.path = "../data/"

    def get_packets_tcp(self, filename):
        cap = pyshark.FileCapture(self.path + filename, display_filter="tcp")
        length = []
        counter = 0
        for packet in cap:
            try:
                counter += 1
                mac_dst = packet.eth.dst
                mac_src = packet.eth.src
                ip_dst = packet.ip.dst
                ip_src = packet.ip.src
                port_dst = packet.tcp.dstport
                port_src = packet.tcp.srcport
                flags = packet.tcp.flags
                window_size = packet.tcp.window_size
                ack_raw = packet.tcp.ack_raw
                seq_raw = packet.tcp.seq_raw
                time = packet.sniff_time

                data = mactob(mac_dst) + mactob(mac_src) + iptob(ip_dst) + iptob(ip_src) + inttob(port_dst) + inttob(port_src) + inttob(window_size) + inttob(ack_raw) + inttob(seq_raw) + inttob(int(flags, 16))
                np_data = ltoa(data)
                length.append(len(np_data))
            except Exception:
                pass
            # if counter == 1000:
            #     break
        print(max(length))


if __name__ == '__main__':
    adapter = Adapter()
    file = "learning_tcp.pcapng"
    Adapter().get_packets_tcp(file)
