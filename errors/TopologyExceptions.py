class TopologySizeException(Exception):
    message = "Wrong topology size in JSON!"


class TopologyMainDiagException(Exception):
    message = "Nodes connected with yourself"


class TopologySymmetryException(Exception):
    message = "All connections must be double-sided"
