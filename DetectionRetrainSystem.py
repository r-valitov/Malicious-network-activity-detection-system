import pyshark

from DetectionSystem import DetectionSystem
from Trainer import Trainer
from enums.Behavior import Behavior
from enums.Kind import Kind
from enums.Mode import Mode
from history.notes.TCPHistoryNote import TCPHistoryNote
from history.notes.UDPHistoryNote import UDPHistoryNote


class DetectionRetrainSystem:
    def __init__(self, hidden_size, model_path, interface="Ethernet"):
        self.interface = interface
        self.action_num = 2

        self.trainer = Trainer(hidden_size, Behavior.TEACH, Mode.HYBRID)
        self.detector = DetectionSystem(hidden_size, interface)

        self.trainer.load_model(model_path)
        self.detector.load_model(model_path)

    def retrain(self, note):
        if self.detector.suspicion <= 0.1:
            self.trainer.retrain(note, 0.5, self.detector.suspicion)

    def run(self):
        try:
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
                self.detector.model.set_protocol(protocol)
                action = self.detector.select_action(note.message)
                if action == 0:
                    attack_counter += 1
                self.detector.analyse(note, action, attack_counter, packet_counter)
                if action == 1:
                    self.retrain(note)
        finally:
            self.detector.reset_firewall()
