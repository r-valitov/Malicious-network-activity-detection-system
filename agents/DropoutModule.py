import torch.nn as nn
import torch


class DropoutModule(nn.Module):
    def __init__(self, env_type, hidden_size):
        super(DropoutModule, self).__init__()
        self.type = env_type
        self.hidden_size = hidden_size

    def change_type(self, env_type):
        self.type = env_type

    def forward(self, state):
        if self.type == -1:
            return state
        filler = 0
        tenzor_type = state.dtype
        mask = torch.zeros(self.hidden_size, dtype=tenzor_type)
        common = int(self.hidden_size/2)
        for i in range(0, common):
            mask[i] = 1
        differ = common + int(self.hidden_size/4)
        if self.type == 0:
            filler = 1
        for i in range(common, differ):
            mask[i] = filler
        if self.type == 0:
            filler = 0
        else:
            filler = 1
        for i in range(differ, self.hidden_size):
            mask[i] = filler
        return state * mask


def test_dropout():
    hidden_size = 128
    a = DropoutModule(env_type=1, hidden_size=hidden_size)
    random_tensor_one_ex = (torch.rand(hidden_size) * 10).int()
    answer = a.forward(random_tensor_one_ex)
    print(answer)
