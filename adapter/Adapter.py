import argparse
import pyshark
import torch
from detector.DetectionSystem import DetectionSystem
from enums.Behavior import Behavior
from utils.Misc import mactob, iptob, inttob, ltoa


class Adapter:
    def __init__(self):
        self.path = "../data/"
        self.args = self.get_args()

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description='PyTorch Actor-Critic malicious network detection system')
        parser.add_argument('--hidden', type=int, default=512, metavar='N', help='Hidden layer size (default: 256)')
        parser.add_argument('--iface', type=str, default="eth0", metavar='N', help='Interface')
        return parser.parse_args()

    def get_packets_tcp(self, filename):
        # detector = DetectionSystem(self.args.hidden)
        # detector.model.load_state_dict(torch.load("saved/model-2020-05-20-17.27.25.a2c"))
        # detector.model.eval()
        # rewards = []
        # state = detector.env.reset()
        # for i in range(1, 100000):
        #     action = detector.select_action(state)
        #     state, reward, done, _ = detector.env.step(action)
        #     rewards.append(reward)
        #
        #     if i % args.log_interval == 0:
        #         print('Episode {}\tLast reward: {:.2f}\tSum reward: {:.2f}'
        #               .format(i, reward, sum(rewards)))
        #
        #
        # for packet in capture.sniff_continuously(packet_count=5):
        #     print
        #     'Just arrived:', packet
        #
        #     capture = pyshark.LiveCapture(interface='eth0')

        cap = pyshark.FileCapture(self.path + filename, display_filter="udp")
        length = []
        counter = 0
        for packet in cap:
            try:
                counter += 1
                mac_dst = packet.eth.dst
                mac_src = packet.eth.src
                ip_dst = packet.ip.dst
                ip_src = packet.ip.src
                port_dst = packet.udp.dstport
                port_src = packet.udp.srcport
                checksum = packet.udp.checksum
                cs_status = packet.udp.checksum_status
                packet_length = packet.udp.length
                stream = packet.udp.stream
                time = packet.sniff_time

                data = mactob(mac_dst) + mactob(mac_src) + iptob(ip_dst) + iptob(ip_src) + inttob(port_dst) + inttob(
                    port_src) + inttob(int(checksum, 16)) + inttob(cs_status) + inttob(stream) + inttob(packet_length)
                np_data = ltoa(data)
                length.append(len(np_data))
            except Exception:
                pass
            # if counter == 1000:
            #     break
        print(max(length))


if __name__ == '__main__':
    adapter = Adapter()
    file = "learning_udp.pcapng"
    Adapter().get_packets_tcp(file)
