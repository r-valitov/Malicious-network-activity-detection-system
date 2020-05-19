from log.TCP.TCPHistory import TCPHistory


class TCPHistorical:
    history = TCPHistory()

    def reset(self):
        self.history.reset()
