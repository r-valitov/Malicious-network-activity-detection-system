from enums.Kind import Kind
import pyshark
from log.TCP.TCPHistorical import TCPHistorical
from log.TCP.TCPHistoryNote import TCPHistoryNote


class TCPGenerator(TCPHistorical):
    def __init__(self):
        self.path = "data/"
        self.learning_file = "learning_tcp.pcapng"
        self.attack_file = "attack_tcp.pcapng"
        self.test_file = "test_tcp.pcapng"
        self.learning_cap = pyshark.FileCapture(self.path + self.learning_file, display_filter="tcp")
        self.attack_cap = pyshark.FileCapture(self.path + self.attack_file, display_filter="tcp")
        self.test_cap = pyshark.FileCapture(self.path + self.test_file, display_filter="tcp")

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
        note = TCPHistoryNote(package, kind)
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
