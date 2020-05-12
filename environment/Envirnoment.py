from enums.Kind import Kind
from network.Network import Network
from enums.Behavior import Behavior
import numpy as np


class Environment:
    network = Network()
    action_space = 2
    observation_space = 8
    info = ""

    def __init__(self, behavior=Behavior.ONLY_SAFE):
        self.done = False
        self.behavior = behavior

    def reset(self):
        self.network.reset()
        self.done = False
        return self.from_message_to_numpy(self.network.step().message)

    @staticmethod
    def from_message_to_numpy(msg):
        arr = np.ndarray((8,), buffer=msg.to_bytes(8, 'big'), dtype=np.int8)
        return arr

    def step(self, action):
        if (action != 0) & (action != 1):
            print("Wrong action")
            return -1, -1, False, ""
        note = self.network.step()
        if (action == 1) & (note.kind == Kind.DANGER):
            reward = 1
        elif (action == 1) & (note.kind == Kind.SAFE):
            reward = -1
        else:
            reward = 0
        observation = self.from_message_to_numpy(note.message)
        done = self.done
        info = note
        return observation, reward, done, info
