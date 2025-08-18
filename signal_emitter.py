from supr_signal import SuprSignal
from signal_color import SignalColor
import psutil
import socket
import dbus


class SignalEmitter:
    def __init__(self):
        self.sig_color = SignalColor(0, 0, 0)

    def unused(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, SignalColor.SEAFOAM)

    def off(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, SignalColor.off())

    def error(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, SignalColor.error())

    def mem(self, sensor=(0, 0)) -> SuprSignal:
        mem = psutil.virtual_memory()
        consumed = mem.total - mem.available
        percent_consumed = (consumed * 100) / mem.total
        color = SignalColor.percentage(percent_consumed)
        return SuprSignal(sensor, color)

    def free_disk(self, path="/", sensor=(0, 0)) -> SuprSignal:
        try:
            if self.is_disk_mounted(path):
                usage = psutil.disk_usage(path)
                percent_used = usage.percent
                color = SignalColor.percentage(percent_used)
            else:
                color = SignalColor.unavail()
        except Exception:
            color = SignalColor.off()

        return SuprSignal(sensor, color)

    def wan(self, hostname, sensor=(0, 0)) -> SuprSignal:
        try:
            with socket.create_connection((hostname, 443), timeout=5):
                return SuprSignal(sensor, SignalColor.get_color_by_switch(True))
        except OSError:
            return SuprSignal(sensor, SignalColor.get_color_by_switch(False))

    def is_disk_mounted(self, mount_point):
        for part in psutil.disk_partitions(all=False):
            if part.mountpoint == mount_point:
                return True
        return False

    def mounts(self, mount_point, sensor=(0, 0)) -> SuprSignal:
        if self.is_disk_mounted(mount_point):
            return SuprSignal(sensor, SignalColor.get_color_by_switch(True))
        return self.unused(sensor)

    def bluetooth(self, sensor=(0, 0)):
        bus = dbus.SystemBus()
        adapter = bus.get_object("org.bluez", "/org/bluez/hci0")
        props = dbus.Interface(adapter, "org.freedesktop.DBus.Properties")
        return SuprSignal(
            sensor,
            SignalColor.get_color_by_switch(props.Get("org.bluez.Adapter1", "Powered")),
        )

    def thermal(self, zone=0, sensor=(0, 0)):
        try:
            with open(f"/sys/class/thermal/thermal_zone{zone}/temp", "r") as f:
                mr = int(f.read().strip())
                r = mr / 1000.0
                return SuprSignal(sensor, SignalColor.percentage(round(r, 1)))
        except Exception:
            return SuprSignal(sensor, SignalColor.unavail())
