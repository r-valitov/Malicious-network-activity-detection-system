import numpy as np
from collections import namedtuple
import torch
import torch.nn.functional as f
import torch.optim as opt
from torch.distributions import Categorical
from agents.ActorCriticModule import ActorCriticModule
from enums.Behavior import Behavior
from enums.Mode import Mode
from Environment import Environment


class DetectionSystem:
    def __init__(self, hidden_size, behavior=Behavior.TEACH, mode=Mode.DEMO):
        super(DetectionSystem, self).__init__()
        self.env = Environment(behavior=behavior, mode=mode)
        self.action_num = self.env.action_space
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = ActorCriticModule(self.env.observation_space, hidden_size, self.action_num).to(self.device)
        self.optimizer = opt.Adam(self.model.parameters(), lr=3e-2)
        self.eps = np.finfo(np.float32).eps.item()

    def save_action(self, action, categorical, state_value):
        action_serializer = namedtuple('action_serializer', ['log_prob', 'value'])
        self.model.saved_actions.append(action_serializer(categorical.log_prob(action), state_value))

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

    def finish_episode(self, gamma):
        current_reward = 0
        saved_actions = self.model.saved_actions
        policy_losses = []
        value_losses = []
        returns = []
        for r in self.model.rewards[::-1]:
            current_reward = r + gamma * current_reward
            returns.insert(0, current_reward)
        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + self.eps)
        for (log_prob, value), current_reward in zip(saved_actions, returns):
            advantage = current_reward - value.item()
            policy_losses.append(-log_prob * advantage)
            torch_current_reward = torch.tensor([current_reward]).cuda()
            value_losses.append(f.smooth_l1_loss(value, torch_current_reward))
        self.optimizer.zero_grad()
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
        loss.backward()
        self.optimizer.step()
        del self.model.rewards[:]
        del self.model.saved_actions[:]
