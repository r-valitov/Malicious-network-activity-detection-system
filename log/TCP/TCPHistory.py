
class TCPHistory:
    log = []
    size = len(log)

    def write(self, note):
        self.log.append(note)

    def reset(self):
        self.log = []

    def print_history(self, k=-1):
        if k == -1:
            k = self.size

        for i in range(0, k):
            note = self.log[i]
            print(note)
