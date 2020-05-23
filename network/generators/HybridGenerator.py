import pyshark
from enums.Kind import Kind
from history.Historical import Historical
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote
from random import choices


class HybridGenerator(Historical):
    def __init__(self):
        self.path = "data/"
        self.tcp = "tcp"
        self.udp = "udp"

        self.current_protocol = self.tcp

        self.learning_tcp_file = "learning_" + self.tcp + ".pcapng"
        self.attack_tcp_file = "attack_" + self.tcp + ".pcapng"
        self.test_tcp_file = "test_" + self.tcp + ".pcapng"

        self.learning_tcp_cap = pyshark.FileCapture(self.path + self.learning_tcp_file, display_filter=self.tcp)
        self.attack_tcp_cap = pyshark.FileCapture(self.path + self.attack_tcp_file, display_filter=self.tcp)
        self.test_tcp_cap = pyshark.FileCapture(self.path + self.test_tcp_file, display_filter=self.tcp)

        self.learning_udp_file = "learning_" + self.udp + ".pcapng"
        self.attack_udp_file = "attack_" + self.udp + ".pcapng"
        self.test_udp_file = "test_" + self.udp + ".pcapng"

        self.learning_udp_cap = pyshark.FileCapture(self.path + self.learning_udp_file, display_filter=self.udp)
        self.attack_udp_cap = pyshark.FileCapture(self.path + self.attack_udp_file, display_filter=self.udp)
        self.test_udp_cap = pyshark.FileCapture(self.path + self.test_udp_file, display_filter=self.udp)

    def get_current_protocol_note(self, package, kind):
        if self.current_protocol == self.tcp:
            return TCPHistoryNote(package, kind)
        if self.current_protocol == self.udp:
            return UDPHistoryNote(package, kind)

    def get_current_protocol_learning_cap(self):
        if self.current_protocol == self.tcp:
            return self.learning_tcp_cap.next()
        if self.current_protocol == self.udp:
            return self.learning_udp_cap.next()

    def reset_current_protocol_learning_cap(self):
        if self.current_protocol == self.tcp:
            self.learning_tcp_cap.reset()
        if self.current_protocol == self.udp:
            self.learning_udp_cap.reset()

    def get_current_protocol_attack_cap(self):
        if self.current_protocol == self.tcp:
            return self.attack_tcp_cap.next()
        if self.current_protocol == self.udp:
            return self.attack_udp_cap.next()

    def reset_current_protocol_attack_cap(self):
        if self.current_protocol == self.tcp:
            self.attack_tcp_cap.reset()
        if self.current_protocol == self.udp:
            self.attack_udp_cap.reset()

    def get_current_protocol_test_cap(self):
        if self.current_protocol == self.tcp:
            return self.test_tcp_cap.next()
        if self.current_protocol == self.udp:
            return self.test_udp_cap.next()

    def reset_current_protocol_test_cap(self):
        if self.current_protocol == self.tcp:
            self.test_tcp_cap.reset()
        if self.current_protocol == self.udp:
            self.test_udp_cap.reset()

    def generate(self, kind=Kind.SAFE):
        package = None
        if choices([0, 1], [0.5, 0.5]) == 0:
            self.current_protocol = self.tcp
        else:
            self.current_protocol = self.udp
        if kind == Kind.SAFE:
            try:
                package = self.get_current_protocol_learning_cap()
            except StopIteration:
                self.reset_current_protocol_learning_cap()
                package = self.get_current_protocol_learning_cap()
        if kind == Kind.DANGER:
            try:
                package = self.get_current_protocol_attack_cap()
            except StopIteration:
                self.reset_current_protocol_attack_cap()
                package = self.get_current_protocol_attack_cap()
        if kind == Kind.TEST:
            try:
                package = self.get_current_protocol_test_cap()
                kind = Kind.SAFE
            except StopIteration:
                self.reset_current_protocol_test_cap()
                package = self.get_current_protocol_test_cap()
        note = self.get_current_protocol_note(package, kind)
        self.history.write(note)

    def run(self, kind=Kind.ALL, i=0):
        if i <= 0:
            while True:
                self.generate(kind)
        else:
            for i in range(0, i):
                self.generate(kind)

    def reset(self):
        self.history.reset()
