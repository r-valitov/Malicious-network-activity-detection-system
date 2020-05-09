from network.Topology import Topology
from network.TrafficGenerator import TrafficGenerator, Kind


class Network:
    def __init__(self):
        self.topology = Topology.from_json()
        self.connections = self.topology.connections
        self.connections_number = self.topology.connections_number
        self.generator = TrafficGenerator(self.connections, 64)
        self.history = self.generator.history

    def reset(self):
        self.generator.reset()

    def step(self):
        self.generator.generate()
        return self.history.log[-1]


e = Network()
e.generator.run(Kind.DANGER, 1000)
e.history.print_history()
