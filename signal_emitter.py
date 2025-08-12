from supr_signal import SuprSignal
from signal_color import SignalColor
import psutil
import socket
import os
import dbus

COLORS = {
    "dark0_hard": SignalColor(40, 40, 40),  # charcoal
    "red": SignalColor(204, 36, 29),  # blood red
    "green": SignalColor(152, 151, 26),  # olive
    "yellow": SignalColor(215, 153, 33),  # amber
    "blue": SignalColor(69, 133, 136),  # teal
    "purple": SignalColor(177, 98, 134),  # mauve
    "aqua": SignalColor(104, 157, 106),  # moss
    "light0": SignalColor(168, 153, 132),  # taupe
    "light1": SignalColor(146, 131, 116),  # clay
    "bright_red": SignalColor(251, 73, 52),  # scarlet
    "bright_green": SignalColor(184, 187, 38),  # lime
    "bright_yellow": SignalColor(250, 189, 47),  # gold
    "bright_blue": SignalColor(131, 165, 152),  # seafoam
    "bright_purple": SignalColor(211, 134, 155),  # rose
    "bright_aqua": SignalColor(142, 192, 124),  # mint
    "light2": SignalColor(235, 219, 178),  # cream
    "dark0": SignalColor(29, 32, 33),  # coal
    "off": SignalColor(0, 0, 0),
}


class SignalEmitter:

    def __init__(self):
        pass

    def get_color(self, num: int) -> SignalColor:
        if num < 50:
            return COLORS["light2"]
        elif num <= 80:
            return COLORS["yellow"]
        elif num <= 100:
            return COLORS["red"]
        else:
            return COLORS["dark0_hard"]

    def get_color_by_switch(self, avail: bool) -> SignalColor:
        return COLORS["light2"] if avail else COLORS["red"]

    def get_color_unavail(self):
        return COLORS["dark0_hard"]
    
    def get_color_unused(self):
        return COLORS["purple"]

    def unused_signal(self, sensor) -> SuprSignal:
        return SuprSignal(sensor, COLORS["purple"])

    def off_signal(self, sensor) -> str:
        return SuprSignal(sensor, COLORS["dark0_hard"])

    def mem_signal(self, sensor=(0, 0)) -> SuprSignal:
        mem = psutil.virtual_memory()
        consumed = mem.total - mem.available
        percent_consumed = (consumed * 100) / mem.total
        color = self.get_color(percent_consumed)
        return SuprSignal(sensor, color)

    def update_workspace_sensor(self, workspace) -> SuprSignal:
        return SuprSignal(workspace, COLORS["green"])

    def free_disk_signal(self, path="/", sensor=(0, 0)) -> SuprSignal:
        try:
            if self.is_disk_mounted(path):
                usage = psutil.disk_usage(path)
                percent_used = usage.percent
                color = self.get_color(percent_used)
            else:
                color = self.get_color_by_switch()
        except:
            color = self.get_color_unused()

        return SuprSignal(sensor, color)

    def wan_signal(self, hostname, sensor=(0, 0)) -> SuprSignal:

        try:
            with socket.create_connection((hostname, 443), timeout=5):
                return SuprSignal(sensor, self.get_color_by_switch(True))
        except OSError:
            return SuprSignal(sensor, self.get_color_by_switch(False))

    def is_disk_mounted(self, mount_point):
        for part in psutil.disk_partitions(all=False):
            if part.mountpoint == mount_point:
                return True

    def mount_signal(self, mount_point, sensor=(0, 0)) -> SuprSignal:
       
        if self.is_disk_mounted(mount_point):
            return SuprSignal(sensor, self.get_color_by_switch(True))

        return self.unused_signal(sensor)

    def bt_signal(self, sensor=(0, 0)):
        bus = dbus.SystemBus()
        adapter = bus.get_object("org.bluez", "/org/bluez/hci0")
        props = dbus.Interface(adapter, "org.freedesktop.DBus.Properties")
        return SuprSignal(
            sensor, self.get_color_by_switch(props.Get("org.bluez.Adapter1", "Powered"))
        )

    def term_signal(self, zone=0, sensor=(0, 0)):
        try:
            with open(f"/sys/class/thermal/thermal_zone{zone}/temp", "r") as f:
                mr = int(f.read().strip())
                r = mr / 1000.0
                return SuprSignal(sensor, self.get_color(round(r, 1)))
        except Exception as e:
            return SuprSignal(sensor, self.get_color_unavail())
