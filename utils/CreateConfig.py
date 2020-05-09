from network.Topology import Topology
import json


def create_test_json():
    nodes = [
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 0]]
    Topology(nodes).to_json()


def create_template():
    config = {'size': 128,
              'masks': [
                  'AA19000000000019',
                  '3219000088000000',
                  '2424242424242424',
                  '3324000000000000',
                  '0000000000000512']
              }
    with open('config/Templates.json', 'w') as outfile:
        json.dump(config, outfile)


create_test_json()
print(Topology.from_json())
