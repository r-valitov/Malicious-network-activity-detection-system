from enums.Behavior import Behavior
from enums.Kind import Kind
from network.Topology import Topology
from network.generators.TrafficGenerator import TrafficGenerator
from random import choices


class Network:
    def __init__(self):
        self.topology = Topology.from_json()
        self.connections = self.topology.connections
        self.connections_number = self.topology.connections_number
        self.generator = TrafficGenerator(self.connections, 64)
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
                self.generator.generate(Kind.SAFE)
            else:
                self.generator.generate(Kind.DANGER)

        return self.history.log[-1]
