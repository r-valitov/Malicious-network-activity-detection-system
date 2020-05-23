from enums.Kind import Kind
from network.demo.Connection import Connection
from utils.Misc import itoa


class HistoryNote:
    connection = Connection()
    message = -1
    kind = Kind.ALL
    mask = -1
    protocol = "demo"

    def __init__(self, connection, message, kind, mask):
        self.connection = connection
        self.message = itoa(message)
        self.kind = kind
        self.mask = mask

    def __repr__(self):
        return f"From node №{self.connection.from_} to node №{self.connection.to_} message: {hex(self.message)} " \
               f"{self.kind} and mask {self.mask} "
