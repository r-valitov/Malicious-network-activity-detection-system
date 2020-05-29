from utils.Misc import mactob, iptob, inttob, ltoa


class UDPHistoryNote:
    def __init__(self, packet, kind):
        self.protocol = "udp"
        self.mac_dst = packet.eth.dst
        self.mac_src = packet.eth.src
        try:
            self.ip_dst = packet.ip.dst
            self.ip_src = packet.ip.src
        except AttributeError:
            self.ip_dst = "0.0.0.0"
            self.ip_src = "0.0.0.0"
        self.port_dst = packet.udp.dstport
        self.port_src = packet.udp.srcport
        self.checksum = packet.udp.checksum
        self.cs_status = packet.udp.checksum_status
        self.packet_length = packet.udp.length
        self.stream = packet.udp.stream
        self.time = packet.sniff_time

        self.kind = kind

        self.message = self.get_raw_bytes()

    def __repr__(self):
        return f"From node №{self.ip_src} to node №{self.ip_dst}, kind {self.kind} "

    def get_raw_bytes(self):
        data = mactob(self.mac_dst) + mactob(self.mac_src) + iptob(self.ip_dst) + iptob(self.ip_src) + inttob(
            self.port_dst) + inttob(self.port_src) + inttob(self.cs_status) + inttob(self.stream) + inttob(
            self.packet_length) + inttob(int(self.checksum, 16))
        return ltoa(data)
