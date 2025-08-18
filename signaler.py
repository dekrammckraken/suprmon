SOCKET_PATH = "/tmp/suprlight.sock"

import socket
from enum import Enum
from signal_emitter import SignalEmitter
from supr_signal import SuprSignal
import dbus

"""
1x0 = first pixel of matrix
"""


class Signaler:

    def __init__(self):
        self.emitter = SignalEmitter()

    def send(self):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(SOCKET_PATH)
                for signal in self.signals:
                    sock.sendall(signal.compose().encode("utf-8"))
                sock.shutdown(socket.SHUT_WR)
        except Exception as e:
            print("Failed to send:\n" + traceback.format_exc())


    def clear_all(self):
        self.clear_row(2)
        self.clear_row(3)
        self.clear_row(4)
        self.clear_row(5)
        self.send()

    def clear_row(self, row: int):
        self.signals = [
            self.emitter.off_signal((row, 0)),
            self.emitter.off_signal((row, 1)),
            self.emitter.off_signal((row, 2)),
            self.emitter.off_signal((row, 3)),
            self.emitter.off_signal((row, 4)),
        ]
        self.send()
    def base(self):
        self.clear_row(2)
        self.add_mem_signal(0)
        self.add_mem_signal(1)
        self.add_unused_signal(2)
        self.add_unused_signal(3)
        self.add_unused_signal(4)
        self.send()

    def thermal(self):
        self.clear_row(3)
        self.add_disk_therm_signal(0, 0)
        self.add_disk_therm_signal(1, 1)
        self.add_disk_therm_signal(2, 2)
        self.add_disk_therm_signal(3, 3)
        self.add_disk_therm_signal(4, 4)
        self.add_disk_therm_signal(5, 5)
        self.send()

    def disks_mounts(self):
        self.clear_row(4)
        self.add_disk_mount_signal("/", 0)
        self.add_disk_mount_signal("/mnt/DataDisk", 1)
        self.add_disk_mount_signal("/mnt/SupportDisk", 2)
        self.add_disk_mount_signal("/mnt/BackupDisk", 3)
        self.add_disk_mount_signal("/mnt/WhiteRabbit", 4)
        self.send()

    def disks_spaces(self):
        self.clear_row(5)
        self.add_disk_free_space_signal("/", 0)
        self.add_disk_free_space_signal("/mnt/DataDisk", 1)
        self.add_disk_free_space_signal("/mnt/SupportDisk", 2)
        self.add_disk_free_space_signal("/mnt/BackupDisk", 3)
        self.add_disk_free_space_signal("/mnt/WhiteRabbit", 4)
        self.send()

    def add_disk_mount_signal(self, mount_point, noled):
        self.signals.append(self.emitter.mount_signal(mount_point, (4, noled)))

    def add_disk_free_space_signal(self, mount_point, noled):
        self.signals.append(self.emitter.free_disk_signal(mount_point, (5, noled)))

    def add_disk_therm_signal(self, termhal_id, noled):
        self.signals.append(self.emitter.term_signal(termhal_id, (3, noled)))

    def add_mem_signal(self, noled):
        self.signals.append(self.emitter.mem_signal((2, noled)))

    def add_bluetooth_signal(self, noled):
        self.signals.append(self.emitter.bt_signal((2, noled)))

    def add_unused_signal(self, noled):
        self.signals.append(self.emitter.unused_signal((2, noled)))
