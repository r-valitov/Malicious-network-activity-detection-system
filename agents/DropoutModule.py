import torch.nn as nn
import torch


class DropoutModule(nn.Module):
    def __init__(self, env_type, hidden_size, device):
        super(DropoutModule, self).__init__()
        self.device = device
        self.type = env_type
        self.hidden_size = hidden_size

    def change_type(self, env_type):
        self.type = env_type

    def forward(self, state):
        if self.device.type != "cpu":
            state = state.cuda()
        if self.type == -1:
            return state
        tensor_type = state.dtype
        mask = torch.zeros(self.hidden_size, dtype=tensor_type)
        common = int(self.hidden_size/2)
        for i in range(0, common):
            mask[i] = 1
        for i in range(common, self.hidden_size):
            if self.type == 0:
                filler = 0
            else:
                filler = 1
            mask[i] = (i + filler) % 2
        if self.device.type != "cpu":
            mask = mask.cuda()
        return state * mask
