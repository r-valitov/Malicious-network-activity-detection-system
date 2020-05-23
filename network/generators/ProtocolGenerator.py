import pyshark
from enums.Kind import Kind
from enums.Mode import Mode
from history.Historical import Historical
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote


class ProtocolGenerator(Historical):
    def __init__(self, mode=Mode.TCP):
        self.path = "data/"
        self.mode = mode
        if mode == Mode.TCP:
            self.protocol = "tcp"
        if mode == Mode.UDP:
            self.protocol = "udp"
        self.learning_file = "learning_" + self.protocol + ".pcapng"
        self.attack_file = "attack_" + self.protocol + ".pcapng"
        self.test_file = "test_" + self.protocol + ".pcapng"
        self.learning_cap = pyshark.FileCapture(self.path + self.learning_file, display_filter=self.protocol)
        self.attack_cap = pyshark.FileCapture(self.path + self.attack_file, display_filter=self.protocol)
        self.test_cap = pyshark.FileCapture(self.path + self.test_file, display_filter=self.protocol)

    def generate(self, kind=Kind.SAFE):
        package = None
        if kind == Kind.SAFE:
            try:
                package = self.learning_cap.next()
            except StopIteration:
                self.learning_cap.reset()
                package = self.learning_cap.next()
        if kind == Kind.DANGER:
            try:
                package = self.attack_cap.next()
            except StopIteration:
                self.attack_cap.reset()
                package = self.attack_cap.next()
        if kind == Kind.TEST:
            try:
                package = self.test_cap.next()
                kind = Kind.SAFE
            except StopIteration:
                self.test_cap.reset()
                package = self.test_cap.next()
        note = None
        if self.mode == Mode.TCP:
            note = TCPHistoryNote(package, kind)
        if self.mode == Mode.UDP:
            note = UDPHistoryNote(package, kind)
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
