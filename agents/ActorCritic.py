import gym
import numpy as np
from collections import namedtuple
import torch
import torch.nn.functional as f
import torch.optim as opt
from torch.distributions import Categorical
from agents.ActorCriticModule import ActorCriticModule


class ActorCritic:
    def __init__(self, env_name='Assault-ram-v0', seed=543):
        super(ActorCritic, self).__init__()
        self.seed = seed
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.env_type = 0 if env_name == "MsPacman-ram-v0" else 1
        self.action_num = len(self.env.unwrapped.get_action_meanings())
        self.model = ActorCriticModule(num_actions=self.action_num, env_type=self.env_type)
        self.optimizer = opt.Adam(self.model.parameters(), lr=3e-2)
        self.eps = np.finfo(np.float32).eps.item()
        self.env.seed(seed)
        torch.manual_seed(seed)

    def change_env(self, env_name):
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.action_num = len(self.env.unwrapped.get_action_meanings())
        self.env.seed(self.seed)
        torch.manual_seed(self.seed)

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
            value_losses.append(f.smooth_l1_loss(value, torch.tensor([current_reward])))
        self.optimizer.zero_grad()
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
        loss.backward()
        self.optimizer.step()
        del self.model.rewards[:]
        del self.model.saved_actions[:]
