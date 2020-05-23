import argparse
import time
from itertools import count
import matplotlib.pyplot as plt
import torch

from detector.DetectionSystem import DetectionSystem
from enums.Behavior import Behavior


def get_path():
    return 'saved/model-{}.a2c'.format(time.strftime('%Y-%m-%d-%H.%M.%S'))


def get_args():
    parser = argparse.ArgumentParser(description='PyTorch Actor-Critic malicious network detection system')
    parser.add_argument('--mode', type=str, default='DEMO', metavar='M', help='DEMO, TCP, UDP, HYBRID')
    parser.add_argument('--gamma', type=float, default=0.9, metavar='G', help='Discount factor (default: 0.9)')
    parser.add_argument('--seed', type=int, default=429, metavar='S', help='Random seed (default: 429)')
    parser.add_argument('--hidden', type=int, default=256, metavar='H', help='Hidden layer size (default: 256)')
    parser.add_argument('--history-interval', type=int, default=10, metavar='L', help='Training logs interval(default: 10)')
    parser.add_argument('--train', action='store_true', help='Train network on training dataset')
    parser.add_argument('--test', action='store_true', help='Test network on test dataset')
    parser.add_argument('--detect', action='store_true', help='Run in detection mode')
    parser.add_argument('--interface', type=str, default='eth0', help="Ethernet interface")
    parser.add_argument('--model', type=str, help="Path to a2c model")
    parser.add_argument('--train-episode', type=int, default=1000, metavar='N', help='Train episode(default: 100000)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.train:
        detector = DetectionSystem(args.hidden, behavior=Behavior.TEACH)
        running_rewards = []
        running_reward = 10
        for i_episode in count(1):
            state, ep_reward = detector.env.reset(), 0
            for _ in range(500):
                action = detector.select_action(state)
                state, reward, done, _ = detector.env.step(action)
                detector.model.rewards.append(reward)
                ep_reward += reward
                if done:
                    break

            running_reward = 0.1 * ep_reward + 0.9 * running_reward
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
    else:
        detector = DetectionSystem(args.hidden, behavior=Behavior.REAL_SIMULATE)
        detector.model.load_state_dict(torch.load("saved/model-2020-05-20-17.27.25.a2c"))
        detector.model.eval()
        rewards = []
        state = detector.env.reset()
        for i in range(1, 100000):
            action = detector.select_action(state)
            state, reward, done, _ = detector.env.step(action)
            rewards.append(reward)

            if i % args.log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tSum reward: {:.2f}'
                      .format(i, reward, sum(rewards)))
