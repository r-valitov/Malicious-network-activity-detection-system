import torch
from torch.distributions import Categorical
from collections import namedtuple


class Actional:
    model = None
    action_num = None

    def select_action(self, state):
        state = torch.from_numpy(state).float()
        probabilities, state_value = self.model(state)
        categorical = Categorical(probabilities)
        action = categorical.sample()
        self.save_action(action, categorical, state_value)
        answer = action.item()
        if answer >= self.action_num:
            answer = 0
        return answer

    def save_action(self, action, categorical, state_value):
        action_serializer = namedtuple('action_serializer', ['log_prob', 'value'])
        self.model.saved_actions.append(action_serializer(categorical.log_prob(action), state_value))
