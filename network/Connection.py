class Connection:
    from_ = -1
    to_ = -1

    def __init__(self, from_=-1, to_=-1):
        self.from_ = from_
        self.to_ = to_

    def serialize(self):
        return {'from': self.from_, 'to': self.to_}

    def deserialize(self, ser):
        self.from_ = ser['from']
        self.to_ = ser['to']
