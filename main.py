import argparse
import time
from itertools import count
import matplotlib.pyplot as plt
import torch

from detector.DetectionSystem import DetectionSystem


def get_path():
    return "saved/model-{}.a2c".format(time.strftime("%Y-%m-%d-%H.%M.%S"))


def get_args():
    parser = argparse.ArgumentParser(description='PyTorch Actor-Critic malicious network detection system')
    parser.add_argument('--gamma', type=float, default=0.9, metavar='G', help='Discount factor (default: 0.9)')
    parser.add_argument('--seed', type=int, default=543, metavar='N', help='Random seed (default: 543)')
    parser.add_argument('--hidden', type=int, default=256, metavar='N', help='Hidden layer size (default: 256)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N', help='Training logs interval(default: 10)')
    parser.add_argument('--train', action='store_true', help='Train network')
    parser.add_argument('--train-episode', type=int, default=100000, metavar='N', help='Train episode(default: 100000)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    detector = DetectionSystem(args.hidden)
    running_rewards = []
    if args.train:
        running_reward = 10
        for i_episode in count(1):
            state, ep_reward = detector.env.reset(), 0
            for _ in range(5000):
                action = detector.select_action(state)
                state, reward, done, _ = detector.env.step(action)
                detector.model.rewards.append(reward)
                ep_reward += reward
                if done:
                    break

            running_reward = 0.01 * ep_reward + 0.99 * running_reward
            running_rewards.append(running_reward)
            detector.finish_episode(args.gamma)

            if i_episode % args.log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'
                      .format(i_episode, ep_reward, running_reward))

            if i_episode == args.train_episode:
                plt.plot(running_rewards)
                plt.xlabel('Episode')
                plt.ylabel('Reward')
                plt.show()
                torch.save(detector.model.state_dict(), get_path())
                break
