from log.Default.History import History


class Historical:
    history = History()

    def reset(self):
        self.history.reset()
