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
        state = state.cuda()
        if self.type == -1:
            return state
        tenzor_type = state.dtype
        mask = torch.zeros(self.hidden_size, dtype=tenzor_type)
        common = int(self.hidden_size/2)
        for i in range(0, common):
            mask[i] = 1
        for i in range(common, self.hidden_size):
            if self.type == 0:
                filler = 0
            else:
                filler = 1
            mask[i] = (i + filler) % 2
        mask = mask.cuda()
        return state * mask


def test_dropout():
    hidden_size = 128
    a = DropoutModule(env_type=0, hidden_size=hidden_size)
    random_tensor_one_ex = (torch.rand(hidden_size) * 10).int()
    answer = a.forward(random_tensor_one_ex)
    print(answer)
