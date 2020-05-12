from enums.Kind import Kind
from network.Network import Network
from enums.Behavior import Behavior


class Environment:
    network = Network()
    action_space = 2
    observation_space = 64
    info = ""

    def __init__(self, behavior=Behavior.ONLY_SAFE):
        self.done = False
        self.behavior = behavior

    def reset(self):
        self.done = False

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
        observation = note.message
        done = self.done
        info = note
        return observation, reward, done, info
