from enums.Kind import Kind
from enums.Mode import Mode
from network.Network import Network
from enums.Behavior import Behavior


class Environment:
    action_space = 2            # Action = 0 - Detected malicious activity
    info = ""                   # Action = 1 - Normal activity

    def __init__(self, mode=Mode.DEMO, behavior=Behavior.ONLY_SAFE):
        self.done = False
        self.behavior = behavior
        self.network = Network(mode)
        self.mode = mode
        if self.mode == Mode.DEMO:
            self.observation_space = 8
        else:
            self.observation_space = 68

    def reset(self):
        self.network.reset()
        self.done = False
        return self.network.step().message

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
        observation = note.message
        done = self.done
        if self.mode == Mode.HYBRID:
            info = note.protocol
        else:
            info = ""
        return observation, reward, done, info
