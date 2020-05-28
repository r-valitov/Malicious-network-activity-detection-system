from collections import namedtuple
import pyshark
import torch
from torch.distributions import Categorical
from Actional import Actional
from agents.ActorCriticModule import ActorCriticModule
from enums.Kind import Kind
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote


class DetectionSystem(Actional):
    def __init__(self, hidden_size, interface="eth0"):
        super(DetectionSystem, self).__init__()
        self.interface = interface
        self.action_num = 2
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = ActorCriticModule(68, hidden_size, self.action_num).to(self.device)

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def run(self):
        attack_counter = 0
        packet_counter = 0
        capture = pyshark.LiveCapture(interface=self.interface, display_filter="tcp or udp")
        for packet in capture.sniff_continuously():
            packet_counter += 1
            protocol = str(packet.transport_layer).lower()
            note = None
            if protocol == 'udp':
                note = UDPHistoryNote(packet, kind=Kind.ALL)
            if protocol == 'tcp':
                note = TCPHistoryNote(packet, kind=Kind.ALL)
            self.model.protocol(protocol)
            action = self.select_action(note.message)
            if action == 0:
                attack_counter += 1
                print('['+str(attack_counter)+' from '+str(packet_counter)+'] Detected malicious activity: '+protocol)
