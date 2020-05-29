from datetime import datetime
import os
import pyshark
import torch
import operator
from Actional import Actional
from agents.ActorCriticModule import ActorCriticModule
from enums.Kind import Kind
from history.Historical import Historical
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote


class DetectionSystem(Actional, Historical):
    def __init__(self, hidden_size, interface="eth0"):
        super(DetectionSystem, self).__init__()
        self.interface = interface
        self.action_num = 2
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = ActorCriticModule(68, hidden_size, self.action_num).to(self.device)

        self.suspicion = 0.0

        self.last_timestamp = datetime.now().timestamp()
        self.last_action = 1
        self.number_rule = 1
        self.blocked_ips = []
        self.firewall_rules_name = "Block IP"

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

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
            if ip not in self.blocked_ips:
                name = f"Block IP {self.number_rule}"
                self.number_rule += 1
                print(f"Added new firewall rule: {name} - {ip}")
                self.block_ip(ip)
                self.blocked_ips.append(ip)

            self.history.reset()

            print(f"[{str(attack_counter)} from {str(packet_counter)}] Detected malicious activity: {note.protocol} "
                  f"suspicion level: {str(self.suspicion)}")
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
