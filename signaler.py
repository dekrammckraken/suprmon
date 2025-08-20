SOCKET_PATH = "/tmp/suprlight.sock"

import socket
import traceback
from signal_emitter import SignalEmitter


class Signaler:
    def __init__(self):
        self.emitter = SignalEmitter()
        self.signals = []

    def send(self):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(SOCKET_PATH)
                for signal in self.signals:
                    print(signal.compose().encode("utf-8"))
                    sock.sendall(signal.compose().encode("utf-8"))
                sock.shutdown(socket.SHUT_WR)
        except Exception:
            print("Failed to send:\n" + traceback.format_exc())
        finally:
            self.signals.clear()

    def clear_all(self):

        self.clear_row(2)
        self.clear_row(3)
        self.clear_row(4)
        self.clear_row(5)
        self.send()        
        
    def clear_row(self, row: int, length=5):

        for col in range(length):
            self.signals.append(self.emitter.off((row, col)))
        

    def base(self):
        self.add_mem(0)
        self.add_mem(1)
        self.add_unused(2)
        self.add_unused(3)
        self.add_unused(4)
        
        self.send()

    def thermal(self):
        self.clear_row(3, length=6)
        for i in range(6):
            self.add_thermal(i, i)

        self.send()
        
    def disks_mounts(self):
        self.clear_row(4)
        mounts = ["/", "/mnt/DataDisk", "/mnt/SupportDisk", "/mnt/BackupDisk", "/mnt/WhiteRabbit"]
        
        for idx, mp in enumerate(mounts):
            self.add_mount(mp, idx)

        self.send()

    def disks_spaces(self):
        
        mounts = ["/", "/mnt/DataDisk", "/mnt/SupportDisk", "/mnt/BackupDisk", "/mnt/WhiteRabbit"]
        
        for idx, mp in enumerate(mounts):
            self.add_free_space(mp, idx)

        self.send()

    def add_mount(self, mount_point, noled):
        self.signals.append(self.emitter.mounts(mount_point, (4, noled)))

    def add_free_space(self, mount_point, noled):
        self.signals.append(self.emitter.free_disk(mount_point, (5, noled)))

    def add_thermal(self, thermal_id, noled):
        self.signals.append(self.emitter.thermal(thermal_id, (3, noled)))

    def add_mem(self, noled):
        self.signals.append(self.emitter.mem((2, noled)))

    def add_bluetooth_signal(self, noled):
        self.signals.append(self.emitter.bluetooth((2, noled)))

    def add_unused(self, noled):
        self.signals.append(self.emitter.unused((2, noled)))

    def add_red(self, noled):
        self.signals.append(self.emitter.error((2, noled)))
