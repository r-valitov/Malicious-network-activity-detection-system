from collections import namedtuple
from datetime import datetime
import os
import pyshark
import torch
import operator

from torch.distributions import Categorical

from AModel import AModel
from agents.ActorCriticModule import ActorCriticModule
from enums.Kind import Kind
from history.Historical import Historical
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote


class DetectionSystem(AModel, Historical):
    def __init__(self, hidden_size, interface="eth0", device="cpu"):
        super(DetectionSystem, self).__init__()
        self.interface = interface
        self.action_num = 2
        self.device = None
        if device != "cpu":
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        self.model = ActorCriticModule(68, hidden_size, self.action_num, self.device).to(self.device)

        self.suspicion = 0.0

        self.last_timestamp = datetime.now().timestamp()
        self.last_action = 1
        self.number_rule = 1
        self.blocked_ips = []
        self.firewall_rules_name = "Block IP"
        self.show_log = True

    def analyse(self, note, action, attack_counter, packet_counter):
        if action == 0:
            note_timestamp = note.time.timestamp()
            if self.last_timestamp - note_timestamp < 0.1 and self.last_action == 0:
                self.suspicion += 0.005
            else:
                self.suspicion += 0.001
        else:
            self.suspicion -= 0.001
        if self.suspicion < 0:
            self.suspicion = 0
        if self.suspicion > 1:
            self.suspicion = 1

        if self.suspicion >= 0.5:
            self.history.log.append(note)
        else:
            self.history.reset()

        if self.suspicion >= 0.8:
            stat = self.get_ip_stat()
            ip = max(stat.items(), key=operator.itemgetter(1))[0]

            if self.show_log:
                print(f"[{str(attack_counter)} from {str(packet_counter)}] Detected malicious activity: {note.protocol} "
                      f"suspicion level: {str(self.suspicion)}")

            if ip not in self.blocked_ips:
                name = f"Block IP {self.number_rule}"
                self.number_rule += 1
                print(f"Added new firewall rule: {name} - {ip}")
                self.block_ip(ip)
                self.blocked_ips.append(ip)
                self.show_log = False

            self.history.reset()
            self.suspicion = 0

    def block_ip(self, ip):
        command = f"netsh advfirewall firewall add rule name=\"{self.firewall_rules_name}\"" \
                  f" dir=in interface=any action=block remoteip={ip}/32"
        os.popen(command)

    def reset_firewall(self):
        command = f"netsh advfirewall firewall delete rule name=\"{self.firewall_rules_name}\""
        os.popen(command)

    def get_ip_stat(self):
        stat = {}
        for note in self.history.log:
            if note.ip_src in stat.keys():
                stat[note.ip_src] += 1
            else:
                stat[note.ip_src] = 1
        return stat

    def run(self):
        attack_counter = 0
        packet_counter = 0
        capture = pyshark.LiveCapture(interface=self.interface, display_filter="tcp or udp")
        for packet in capture.sniff_continuously():
            start_time = datetime.now()
            packet_counter += 1
            protocol = str(packet.transport_layer).lower()
            note = None
            if protocol == 'udp':
                note = UDPHistoryNote(packet, kind=Kind.ALL)
            if protocol == 'tcp':
                note = TCPHistoryNote(packet, kind=Kind.ALL)
            self.model.set_protocol(protocol)
            action = self.select_action(note.message)
            if action == 0:
                attack_counter += 1
            self.analyse(note, action, attack_counter, packet_counter)
            end_time = datetime.now()
            delta = end_time - start_time
            if self.show_log:
                print(f"[{delta.microseconds / 1000} ms] Current suspicion value: {self.suspicion}")

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
