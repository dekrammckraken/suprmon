from supr_signal import SuprSignal
from signal_color import SignalColor
import psutil
import socket
import dbus


class SignalEmitter:

    def mem(self, sensor) -> SuprSignal:
        mem = psutil.virtual_memory()
        consumed = mem.total - mem.available
        percent_consumed = int((consumed * 100) / mem.total)
        color = SignalColor.percentage(percent_consumed)
        return SuprSignal(sensor, color)

    def custom(self, color: SignalColor, sensor) -> SuprSignal:
        return SuprSignal(sensor, color)

    def free_disk(self, path, sensor) -> SuprSignal:
        try:
            if self.is_disk_mounted(path):
                usage = psutil.disk_usage(path)
                percent_used = int(usage.percent)
                color = SignalColor.percentage(percent_used)
            else:
                color = SignalColor.off()
        except Exception:
            color = SignalColor.off()

        return SuprSignal(sensor, color)

    def wan(self, hostname, sensor) -> SuprSignal:
        try:
            with socket.create_connection((hostname, 443), timeout=5):
                return SuprSignal(sensor, SignalColor.on_off(True))
        except OSError:
            return SuprSignal(sensor, SignalColor.on_off(False))

    def is_disk_mounted(self, mount_point):
        for part in psutil.disk_partitions(all=False):
            if part.mountpoint == mount_point:
                return True
        return False

    def mounts(self, mount_point, sensor) -> SuprSignal:
        if self.is_disk_mounted(mount_point):
            return SuprSignal(sensor, SignalColor.on_off(True))
        return self.off(sensor)

    def bluetooth(self, sensor) -> SuprSignal:
        bus = dbus.SystemBus()
        adapter = bus.get_object("org.bluez", "/org/bluez/hci0")
        props = dbus.Interface(adapter, "org.freedesktop.DBus.Properties")
        powered = props.Get("org.bluez.Adapter1", "Powered")
        return SuprSignal(sensor, SignalColor.on_off(powered))

    def thermal(self, zone, sensor) -> SuprSignal:
        try:
            with open(f"/sys/class/thermal/thermal_zone{zone}/temp", "r") as f:
                temp_milli = int(f.read().strip())
                temp_c = int(temp_milli / 1000)
                return SuprSignal(sensor, SignalColor.percentage(temp_c))
        except Exception:
            return SuprSignal(sensor, SignalColor.off())

    def unused(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, SignalColor.unused())

    def off(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, SignalColor.off())

    def custom(self, color: SignalColor, sensor) -> SuprSignal:
        return SuprSignal(sensor, color)
