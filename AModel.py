import torch
from torch.distributions import Categorical
from collections import namedtuple


class AModel:
    model = None
    action_num = None

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
