import random
from environment.SecurityTemplate import SecurityTemplate
from log.Default.Historical import Historical
from enums.Kind import Kind
from log.Default.HistoryNote import HistoryNote


class TrafficGenerator(Historical):
    checker = SecurityTemplate()

    def __init__(self, connections, size):
        self.connections = connections
        self.connections_number = len(self.connections)
        self.message_size = size

    def generate(self, kind=Kind.ALL):
        connection_index = random.randint(0, self.connections_number - 1)
        connection = self.connections[connection_index]
        message = random.getrandbits(self.message_size)
        mask = -1
        if kind == Kind.SAFE:
            while True:
                if not self.checker.check(message):
                    break
                message = random.getrandbits(self.message_size)
        if kind == Kind.DANGER:
            while True:
                check, tmp = self.checker.check_with_mask(message)
                if check:
                    mask = tmp
                    break
                message = random.getrandbits(self.message_size)
        if kind == Kind.ALL:
            if self.checker.check(message):
                kind = Kind.DANGER
            else:
                kind = Kind.SAFE
        self.history.write(HistoryNote(connection, message, kind, mask))

    def run(self, kind=Kind.ALL, i=0):
        if i <= 0:
            while True:
                self.generate(kind)
        else:
            for i in range(0, i):
                self.generate(kind)

    def reset(self):
        self.history.reset()
