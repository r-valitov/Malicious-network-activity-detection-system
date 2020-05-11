import argparse
import time


def get_path():
    return "saved/model-{}.a2c".format(time.strftime("%Y-%m-%d-%H.%M.%S"))


def get_args():
    parser = argparse.ArgumentParser(description='PyTorch Actor-Critic malicious network detection system')
    parser.add_argument('--gamma', type=float, default=0.9, metavar='G', help='discount factor (default: 0.90)')
    parser.add_argument('--seed', type=int, default=543, metavar='N', help='random seed (default: 543)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N', help='training logs interval(default: 10)')
    parser.add_argument('--train', action='store_true', help='train network')
    parser.add_argument('--train-episode', type=int, default=100000, metavar='N', help='train episode(default: 100000)')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()


# from environment.Envirnoment import Environment
#
# env = Environment()
# for i_episode in range(20):
#     for t in range(100):
#         action = env.action_space
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
