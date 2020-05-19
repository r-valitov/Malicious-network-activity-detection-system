from enums.Kind import Kind
from network.Network import Network
from enums.Behavior import Behavior
from utils.Misc import itoa


class Environment:
    network = Network()
    action_space = 2            # Action = 0 - Detected malicious activity
    observation_space = 8       # Action = 1 - Normal activity
    info = ""

    def __init__(self, behavior=Behavior.ONLY_SAFE):
        self.done = False
        self.behavior = behavior

    def reset(self):
        self.network.reset()
        self.done = False
        return itoa(self.network.step().message)

    def step(self, action):
        if (action != 0) & (action != 1):
            print("Wrong action")
            return -1, -1, False, ""
        note = self.network.step(self.behavior)
        if (action == 1) & (note.kind == Kind.DANGER):
            reward = 1
        elif (action == 1) & (note.kind == Kind.SAFE):
            reward = -1
        elif (action == 0) & (note.kind == Kind.SAFE):
            reward = 1
        else:
            reward = -1
        observation = itoa(note.message)
        done = self.done
        info = note
        return observation, reward, done, info
