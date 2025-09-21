SOCKET_PATH = "/tmp/suprlight.sock"

import socket
import traceback
from signal_emitter import SignalEmitter
from signal_color import SignalColor
import time


class Signaler:
    def __init__(self):
        self.emitter = SignalEmitter()
        self.signals = []
        self.animating = False

    def send(self):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(SOCKET_PATH)
                for signal in self.signals:
                    #print(signal.compose().encode("utf-8"))
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

    def fill_row(self, color, row: int, length=5):

        for col in range(length):
            self.signals.append(self.emitter.custom(color, (row, col)))

    def reboot(self):
        self.fill_row(SignalColor.SCARLET, 1)
        self.send()

    def halt(self):
        self.fill_row(SignalColor.BLOOD_RED, 1)
        self.send()

    def tty_error(self):
        self.fill_row(SignalColor.BLOOD_RED, 1)
        self.send()

    def tty_success(self):
        self.fill_row(SignalColor.OLIVE, 1)
        self.send()

    def cancel(self):
        self.fill_row(SignalColor.OFF, 1)
        self.fill_row(SignalColor.OFF, 2)
        self.fill_row(SignalColor.OFF, 3)
        self.fill_row(SignalColor.OFF, 4)
        self.fill_row(SignalColor.OFF, 5)
        self.send()

    def base(self):
        self.mem(0)

        self.send()

    def thermals(self):
        self.thermal(0, 0) #acpitz
        self.thermal(1, 1) #acpitz
        self.thermal(2, 2) #pch_skylake
        self.thermal(3, 3) #cpu
        self.thermal_gpu(4) #gpu
        self.send()

    def disks_mounts(self):
        mounts = [
            "/",
            "/mnt/DataDisk",
            "/mnt/SupportDisk",
            "/mnt/BackupDisk",
            "/mnt/WhiteRabbit",
        ]

        for idx, mp in enumerate(mounts):
            self.mount_point(mp, idx)

        self.send()

    def disks_spaces(self):

        mounts = [
            "/",
            "/mnt/DataDisk",
            "/mnt/SupportDisk",
            "/mnt/BackupDisk",
            "/mnt/WhiteRabbit",
        ]

        for idx, mp in enumerate(mounts):
            self.free_space(mp, idx)

        self.send()

    def vpn(self, noled):
        self.signals.append(self.emitter.vpn((2, noled)))

    def mem(self, noled):
        self.signals.append(self.emitter.mem((2, noled)))

    def mount_point(self, mount_point, noled):
        self.signals.append(self.emitter.mounts(mount_point, (4, noled)))

    def free_space(self, mount_point, noled):
        self.signals.append(self.emitter.free_disk(mount_point, (5, noled)))

    def thermal(self, zone_id, noled):
        self.signals.append(self.emitter.thermal(zone_id, (3, noled)))

    def thermal_gpu(self, noled):
         self.signals.append(self.emitter.thermal_gpu((3, noled)))

    def bluetooth(self, noled):
        self.signals.append(self.emitter.bluetooth((2, noled)))

    def unused(self, noled):
        self.signals.append(self.emitter.unused((2, noled)))

    def help(self):
        print("=== Atom LED Panel ===")
        print("○ ○ ○ ○ ○ = <mem,off,off,off,off>")
        print("○ ○ ○ ○ ○ = <acpi,acpi,controller,cpu,off,gpu>")
        print("○ ○ ○ ○ ○ = <mnt1,mnt2,mnt3,mnt4,mnt5>")
        print("○ ○ ○ ○ ○ = <fspace1,fspace2,fspace3,fspace4,fspace5>")
