import argparse
import time
import torch
from itertools import count
import matplotlib.pyplot as plt
from temp.ActorCritic import ActorCritic
from agents.DropoutModule import DropoutModule


def get_path():
    return "saved/model-{}.a2c".format(time.strftime("%Y-%m-%d-%H.%M.%S"))


def get_args():
    parser = argparse.ArgumentParser(description='PyTorch actor-critic example')
    parser.add_argument('--gamma', type=float, default=0.9, metavar='G', help='discount factor (default: 0.90)')
    parser.add_argument('--seed', type=int, default=543, metavar='N', help='random seed (default: 543)')
    parser.add_argument('--render', action='store_true', help='render the environment')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='training logs interval(default: 10)')
    parser.add_argument('--train', action='store_true', help='train network')
    parser.add_argument('--train-episode', type=int, default=100000, metavar='N',
                        help='train episode(default: 100000)')
    parser.add_argument('--execute', action='store_true', help='execute one game')
    parser.add_argument('--env-name', type=str, default='MsPacman-ram-v0', help='Name of Atari game')
    return parser.parse_args()


def main():
    args = get_args()
    a2c = ActorCritic(args.env_name)
    running_rewards = []
    if args.train:
        running_reward = 10
        for i_episode in count(1):
            state, ep_reward = a2c.env.reset(), 0
            for _ in range(5000):
                action = a2c.select_action(state)
                state, reward, done, _ = a2c.env.step(action)
                if args.render:
                    a2c.env.render()
                a2c.model.rewards.append(reward)
                ep_reward += reward
                if done:
                    break

            running_reward = 0.1 * ep_reward + 0.9 * running_reward
            running_rewards.append(running_reward)
            a2c.finish_episode(args.gamma)

            if i_episode % args.log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'
                      .format(i_episode, ep_reward, running_reward))

            if i_episode == args.train_episode:
                plt.plot(running_rewards)
                plt.xlabel('Episode')
                plt.ylabel('Reward')
                plt.show()
                torch.save(a2c.model.state_dict(), get_path())
                break


def dropout_main():
    packman = "MsPacman-ram-v0"
    assault = "Assault-ram-v0"
    args = get_args()
    a2c = ActorCritic(packman)
    running_rewards = []
    if args.train:
        running_reward = 10
        for i_episode in count(1):
            state, ep_reward = a2c.env.reset(), 0
            for _ in range(5000):
                action = a2c.select_action(state)
                state, reward, done, _ = a2c.env.step(action)
                if args.render:
                    a2c.env.render()
                a2c.model.rewards.append(reward)
                ep_reward += reward
                if done:
                    break

            running_reward = 0.1 * ep_reward + 0.9 * running_reward
            running_rewards.append(running_reward)
            a2c.finish_episode(args.gamma)

            if i_episode % args.log_interval == 0:
                print('Game {}\tEpisode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'
                      .format(a2c.env_name, i_episode, ep_reward, running_reward))

            if i_episode % args.train_episode == 0:
                plt.plot(running_rewards)
                plt.xlabel('Episode')
                plt.ylabel('Reward')
                plt.show()
                torch.save(a2c.model.state_dict(), get_path())
                if a2c.env_name == packman:
                    a2c.change_env(assault)
                else:
                    a2c.change_env(packman)


def test_dropout():
    hidden_size = 128
    a = DropoutModule(env_type=1, hidden_size=hidden_size)
    random_tensor_one_ex = (torch.rand(hidden_size) * 10).int()
    answer = a.forward(random_tensor_one_ex)
    print(answer)


if __name__ == '__main__':
    # test_dropout()
    dropout_main()
