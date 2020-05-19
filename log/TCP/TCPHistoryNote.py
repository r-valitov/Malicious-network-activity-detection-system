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

    def __repr__(self):
        return f"From node №{self.ip_src} to node №{self.ip_dst}, kind {self.kind} "
