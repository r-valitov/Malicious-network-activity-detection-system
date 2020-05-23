from network.generators.TCPGenerator import TCPGenerator
from enums.Behavior import Behavior
from enums.Kind import Kind
from random import choices


class TCPNetwork:
    def __init__(self):
        self.generator = TCPGenerator()
        self.history = self.generator.history

    def reset(self):
        self.generator.reset()

    def step(self, behavior=Behavior.ONLY_SAFE):
        if behavior == Behavior.ONLY_SAFE:
            self.generator.generate(Kind.SAFE)
        if behavior == Behavior.ONLY_DANGER:
            self.generator.generate(Kind.DANGER)
        if behavior == Behavior.TEACH:
            if choices([0, 1], [0.5, 0.5]) == 0:
                self.generator.generate(Kind.SAFE)
            else:
                self.generator.generate(Kind.DANGER)
        if behavior == Behavior.REAL_SIMULATE:
            if choices([0, 1], [0.98, 0.02]) == 0:
                self.generator.generate(Kind.TEST)
            else:
                self.generator.generate(Kind.DANGER)
        return self.history.log[-1]
