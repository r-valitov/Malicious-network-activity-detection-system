import torch.nn as nn
import torch.nn.functional as func
from agents.DropoutModule import DropoutModule


class ActorCriticModule(nn.Module):
    def __init__(self, num_inputs, hidden_size, num_actions, env_type):
        super(ActorCriticModule, self).__init__()
        self.num_actions = num_actions
        self.network_input = nn.Linear(num_inputs, hidden_size)
        self.env_type = env_type
        self.network_dropout = DropoutModule(env_type=env_type, hidden_size=hidden_size)
        self.action_head = nn.Linear(hidden_size, num_actions)
        self.value_head = nn.Linear(hidden_size, 1)
        self.saved_actions = []
        self.rewards = []

    def forward(self, state):
        h = func.relu(self.network_input(state))
        h = self.network_dropout(h)
        action_scores = self.action_head(h)
        value = self.value_head(h)
        return func.softmax(action_scores, dim=-1), value
