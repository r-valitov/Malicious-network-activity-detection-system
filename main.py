import argparse
import time
from itertools import count
import matplotlib.pyplot as plt
import torch

from DetectionSystem import DetectionSystem
from Trainer import Trainer
from enums.Behavior import Behavior
from enums.Mode import Mode


def get_path():
    return 'saved/model-{}.a2c'.format(time.strftime('%Y-%m-%d-%H.%M.%S'))


def get_args():
    parser = argparse.ArgumentParser(description='PyTorch Actor-Critic malicious network detection system')
    parser.add_argument('--mode', type=str, default='DEMO', metavar='M', help='DEMO, TCP, UDP, HYBRID (default: DEMO)')
    parser.add_argument('--gamma', type=float, default=0.9, metavar='G', help='Discount factor (default: 0.9)')
    parser.add_argument('--seed', type=int, default=429, metavar='S', help='Random seed (default: 429)')
    parser.add_argument('--hidden', type=int, default=256, metavar='H', help='Hidden layer size (default: 256)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='L', help='Training logs interval(default: 10)')
    parser.add_argument('--train', action='store_true', help='Train network on training dataset')
    parser.add_argument('--train_epoch_size', type=int, default=500, help='Train epoch size')
    parser.add_argument('--test', action='store_true', help='Test network on test dataset')
    parser.add_argument('--test_epochs', type=int, default=10000, help='Test epoch number')
    parser.add_argument('--detect', action='store_true', help='Run in detection mode')
    parser.add_argument('--interface', type=str, default='eth0', help="Ethernet interface")
    parser.add_argument('--model', type=str, help="Path to a2c model")
    parser.add_argument('--train-episode', type=int, default=100000, metavar='N', help='Train episode(default: 100000)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    mode = Mode[args.mode]
    hidden = args.hidden

    if args.train:
        behavior = Behavior.TEACH
        trainer = Trainer(hidden, behavior=behavior, mode=mode)
        running_rewards = []
        running_reward = 10
        epoch_size = args.train_epoch_size
        for i_episode in count(1):
            state, ep_reward = trainer.env.reset(), 0
            for _ in range(epoch_size):
                action = trainer.select_action(state)
                state, reward, done, protocol = trainer.env.step(action)
                trainer.model.rewards.append(reward)
                trainer.model.protocol(protocol)
                ep_reward += reward
                if done:
                    break
            running_reward = 0.1 * ep_reward + 0.9 * running_reward
            running_rewards.append(running_reward)
            trainer.finish_episode(args.gamma)
            if i_episode % args.log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'
                      .format(i_episode, ep_reward, running_reward))
            if i_episode == args.train_episode:
                plt.plot(running_rewards)
                plt.xlabel('Episode')
                plt.ylabel('Reward')
                plt.show()
                torch.save(trainer.model.state_dict(), get_path())
                break
    if args.test:
        model = args.model
        epochs = args.test_epochs
        behavior = Behavior.REAL_SIMULATE
        trainer = Trainer(args.hidden, behavior=behavior, mode=mode)
        trainer.model.load_state_dict(torch.load(model))
        trainer.model.eval()
        rewards = []
        state = trainer.env.reset()
        for i in range(1, epochs):
            action = trainer.select_action(state)
            state, reward, done, protocol = trainer.env.step(action)
            trainer.model.protocol(protocol)
            rewards.append(reward)
            if i % args.log_interval == 0:
                print('Episode {}\tLast reward: {:.2f}\tSum reward: {:.2f}'
                      .format(i, reward, sum(rewards)))

    if args.detect:
        model = args.model
        iface = args.interface
        detector = DetectionSystem(hidden, iface)
        detector.load_model(model)
        detector.run()
