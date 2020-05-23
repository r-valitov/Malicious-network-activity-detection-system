from enums.Behavior import Behavior
from enums.Kind import Kind
from enums.Mode import Mode
from network.demo.Topology import Topology
from network.generators.HybridGenerator import HybridGenerator
from network.generators.ProtocolGenerator import ProtocolGenerator
from network.generators.TrafficGenerator import TrafficGenerator
from random import choices


class Network:
    def __init__(self, mode=Mode.DEMO):
        if mode == Mode.DEMO:
            topology = Topology.from_json()
            self.generator = TrafficGenerator(topology.connections, 64)
        if mode == Mode.TCP or mode == Mode.UDP:
            self.generator = ProtocolGenerator(mode)
        if mode == Mode.HYBRID:
            self.generator = HybridGenerator()
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
            if choices([0, 1], [0.8, 0.2]) == 0:
                self.generator.generate(Kind.SAFE)
            else:
                self.generator.generate(Kind.DANGER)
        return self.history.log[-1]
