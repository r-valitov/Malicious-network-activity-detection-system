
class History:
    log = []
    size = len(log)

    def write(self, note):
        self.log.append(note)

    def reset(self):
        self.log = []

    def print_history(self, k=100):
        for i in range(0, k):
            note = self.log[i]
            connect = note.connection
            from_ = connect.from_
            to_ = connect.to_
            msg = note.message
            kind = note.kind
            mask = note.mask
            print(f"From node №{from_} "
                  f"to node №{to_} message: {hex(msg)} "
                  f"{kind} and mask {hex(mask)}")
