from collections import namedtuple

import numpy as np
from itertools import count
import torch
import torch.nn.functional as f
import torch.optim as opt
import matplotlib.pyplot as plt
from torch.distributions import Categorical

from AModel import AModel
from agents.ActorCriticModule import ActorCriticModule
from enums.Behavior import Behavior
from enums.Mode import Mode
from Environment import Environment
from utils.Misc import get_path


class Trainer(AModel):
    def __init__(self, hidden_size, behavior=Behavior.TEACH, mode=Mode.DEMO, device="cpu"):
        super(Trainer, self).__init__()
        self.env = Environment(behavior=behavior, mode=mode)
        self.action_num = self.env.action_space

        self.device = None
        if device != "cpu":
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model = ActorCriticModule(self.env.observation_space, hidden_size, self.action_num, self.device)\
            .to(self.device)
        self.optimizer = opt.Adam(self.model.parameters(), lr=3e-2)
        self.eps = np.finfo(np.float32).eps.item()
        self.retrain_counter = 0

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
            torch_current_reward = torch.tensor([current_reward]).to(self.device)
            value_losses.append(f.smooth_l1_loss(value, torch_current_reward))
        self.optimizer.zero_grad()
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
        loss.backward()
        self.optimizer.step()
        del self.model.rewards[:]
        del self.model.saved_actions[:]

    def test(self, epochs, log_interval):
        rewards = []
        state = self.env.reset()
        for i in range(1, epochs):
            action = self.select_action(state)
            state, reward, done, protocol = self.env.step(action)
            self.model.set_protocol(protocol)
            rewards.append(reward)
            if i % log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tSum reward: {:.2f}'
                      .format(i, reward, sum(rewards)))

    def retrain(self, note, gamma, suspicion):
        print(f"Retrain in suspicion level: {suspicion}")
        running_rewards = []
        running_reward = 10
        ep_reward = 0
        action = self.select_action(note.get_raw_bytes())
        state, reward, done, protocol = self.env.step(action)
        self.model.rewards.append(reward)
        self.model.set_protocol(protocol)
        ep_reward += reward
        running_reward = 0.1 * ep_reward + 0.9 * running_reward
        running_rewards.append(running_reward)
        self.finish_episode(gamma)
        self.retrain_counter += 1

        if self.retrain_counter == 10000:
            self.save()
            self.retrain_counter = 0

    def save(self):
        path = get_path()
        torch.save(self.model.state_dict(), path)
        print(f"Saving model after training: {path}")

    def train(self, epoch_size, gamma, log_interval, train_episode):
        running_rewards = []
        running_reward = 10
        for i_episode in count(1):
            state, ep_reward = self.env.reset(), 0
            for _ in range(epoch_size):
                action = self.select_action(state)
                state, reward, done, protocol = self.env.step(action)
                self.model.rewards.append(reward)
                self.model.set_protocol(protocol)
                ep_reward += reward
                if done:
                    break
            running_reward = 0.1 * ep_reward + 0.9 * running_reward
            running_rewards.append(running_reward)
            self.finish_episode(gamma)
            if i_episode % log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'
                      .format(i_episode, ep_reward, running_reward))
            if i_episode == train_episode:
                plt.plot(running_rewards)
                plt.xlabel('Episode')
                plt.ylabel('Reward')
                plt.show()
                self.save()
                break

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
