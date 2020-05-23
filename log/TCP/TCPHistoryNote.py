from utils.Misc import mactob, iptob, inttob, ltoa


class TCPHistoryNote:
    def __init__(self, packet, kind):
        self.mac_dst = packet.eth.dst
        self.mac_src = packet.eth.src
        self.ip_dst = packet.ip.dst
        self.ip_src = packet.ip.src
        self.port_dst = packet.tcp.dstport
        self.port_src = packet.tcp.srcport
        self.flags = packet.tcp.flags
        self.window_size = packet.tcp.window_size
        self.ack_raw = packet.tcp.ack_raw
        self.seq_raw = packet.tcp.seq_raw
        self.time = packet.sniff_time

        self.kind = kind

        self.message = self.get_raw_bytes()

    def __repr__(self):
        return f"From node №{self.ip_src} to node №{self.ip_dst}, kind {self.kind} "

    def get_raw_bytes(self):
        data = mactob(self.mac_dst) + mactob(self.mac_src) + iptob(self.ip_dst) + iptob(self.ip_src) + inttob(
            self.port_dst) + inttob(self.port_src) + inttob(self.window_size) + inttob(self.ack_raw) + inttob(
            self.seq_raw) + inttob(int(self.flags, 16))
        return ltoa(data)
