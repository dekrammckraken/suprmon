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
                for signal in self.dashboard:
                    sock.sendall(signal.compose().encode("utf-8"))
                sock.shutdown(socket.SHUT_WR)
        except Exception as e:
            print(f"Failed to send: {e}")

    def reset(self):
        self.dashboard = [
            self.emitter.off_signal((2,0)),
            self.emitter.off_signal((2,1)),
            self.emitter.off_signal((2,2)),
            self.emitter.off_signal((2,3)),
            self.emitter.off_signal((2,4)),
            
            self.emitter.off_signal((3,0)),
            self.emitter.off_signal((3,1)),
            self.emitter.off_signal((3,2)),
            self.emitter.off_signal((3,3)),
            self.emitter.off_signal((3,4)),

            self.emitter.off_signal((4,0)),
            self.emitter.off_signal((4,1)),
            self.emitter.off_signal((4,2)),
            self.emitter.off_signal((4,3)),
            self.emitter.off_signal((4,4)),
    
            self.emitter.off_signal((5,0)),
            self.emitter.off_signal((5,1)),
            self.emitter.off_signal((5,2)),
            self.emitter.off_signal((5,3)),
            self.emitter.off_signal((5,4)),
        ]

    def dash(self):
        self.dashboard = [
            #Core info
            self.emitter.mem_signal((2,0)),
            self.emitter.mem_signal((2,1)),
            self.emitter.bt_signal((2,2)),
            self.emitter.off_signal((2,3)),
            self.emitter.off_signal((2,4)),

            #termal
            self.emitter.term_signal(0, (3,0)),
            self.emitter.term_signal(1, (3,1)),
            self.emitter.term_signal(2, (3,2)),
            self.emitter.term_signal(3, (3,3)),
            self.emitter.term_signal(4, (3,4)),

            #Mounted disks
            self.emitter.mount_signal("/", (4,0)),
            self.emitter.mount_signal("/mnt/DataDisk", (4,1)),
            self.emitter.mount_signal("/mnt/SupportDisk", (4,2)),
            self.emitter.mount_signal("/mnt/BackupDisk", (4,3)),
            self.emitter.mount_signal("/mnt/WhiteRabbit", (4,4)),
            
            #Free space
            self.emitter.fdisk_signal("/", (5,0)),
            self.emitter.fdisk_signal("/mnt/DataDisk", (5,1)),
            self.emitter.fdisk_signal("/mnt/SupportDisk", (5,2)),
            self.emitter.fdisk_signal("/mnt/BackupDisk", (5,3)),
            self.emitter.fdisk_signal("/mnt/WhiteRabbit", (5,4))
        ]

    def update(self):
        self.reset()
        self.dash()
        self.send()
