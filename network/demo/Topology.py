import json
from errors.TopologyExceptions import TopologySizeException, TopologyMainDiagException, TopologySymmetryException
from network.Connection import Connection
from network.WithConnections import WithConnections


class Topology(WithConnections):
    _path = "config/Network.json"

    nodes_number = 0
    nodes = []

    def __init__(self, nodes):
        self.nodes = nodes
        self.nodes_number = len(nodes)
        self.connections = self.get_connects()
        self.connections_number = len(self.connections)

    def __repr__(self):
        representation = ""
        representation += f"The network consists of {self.nodes_number} nodes:\n"
        for index, node in enumerate(self.nodes):
            indexes = [i for i, v in enumerate(node) if v == 1]
            representation += f"Node №{index} connected with {indexes} nodes:\n"
        return representation

    @classmethod
    def from_json(cls, path=""):
        if path == "":
            path = cls._path
        with open(path) as config:
            raw = json.load(config)
            if cls.check(raw):
                return cls(raw['nodes'])

    def to_json(self, path=""):
        if path == "":
            path = self._path
        with open(path, 'w') as outfile:
            json.dump(self.serialize(), outfile)

    @staticmethod
    def check_size(arr, size):
        if len(arr) != size:
            raise TopologySizeException()
        for _ in arr:
            if len(arr) != size:
                raise TopologySizeException()

    @staticmethod
    def check_main_diag(arr, size):
        if len([i for i in range(0, size) if arr[i][i] != 0]) != 0:
            raise TopologyMainDiagException()

    @staticmethod
    def check_sym_diag(arr, size):
        for i in range(0, size):
            for j in range(0, size):
                if arr[i][j] != arr[j][i]:
                    raise TopologySymmetryException()

    @staticmethod
    def check(config):
        size = config['nodes_number']
        arr = config['nodes']
        Topology.check_size(arr, size)
        Topology.check_main_diag(arr, size)
        Topology.check_sym_diag(arr, size)
        return True

    def has_connect(self, i, j):
        if self.nodes[i][j] == 1:
            return True
        return False

    def get_connects(self):
        con = []
        for i in range(0, self.nodes_number):
            for j in range(0, self.nodes_number):
                if self.nodes[i][j] == 1:
                    con.append(Connection(i, j))
        return con

    def serialize(self):
        return {'nodes_number': self.nodes_number, 'nodes': self.nodes}

    def deserialize(self, ser):
        if self.check(ser):
            self.nodes_number = ser['nodes_number']
            self.nodes = ser['nodes']

    def reset(self):
        self.nodes_number = 0
        self.nodes = []
        self.connections = []
        self.connections_number = 0
