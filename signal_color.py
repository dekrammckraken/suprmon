from enum import Enum


class SignalColor(Enum):
    CHARCOAL = (40, 40, 40)
    BLOOD_RED = (204, 36, 29)
    OLIVE = (152, 151, 26)
    AMBER = (215, 153, 33)
    TEAL = (69, 133, 136)
    MAUVE = (177, 98, 134)
    MOSS = (104, 157, 106)
    TAUPE = (168, 153, 132)
    CLAY = (146, 131, 116)
    SCARLET = (251, 73, 52)
    LIME = (184, 187, 38)
    GOLD = (250, 189, 47)
    SEAFOAM = (131, 165, 152)
    ROSE = (211, 134, 155)
    MINT = (142, 192, 124)
    CREAM = (235, 219, 178)
    COAL = (29, 32, 33)
    OFF = (0, 0, 0)

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    @classmethod
    def percentage(cls, num: int):
        if num < 50:
            return cls.CREAM
        elif num < 80:
            return cls.AMBER
        elif num < 100:
            return cls.BLOOD_RED
        else:
            return cls.COAL

    @classmethod
    def on_off(cls, avail: bool):
        return cls.CREAM if avail else cls.BLOOD_RED

    @classmethod
    def unavail(cls):
        return cls.CHARCOAL

    @classmethod
    def unused(cls):
        return cls.CHARCOAL

    @classmethod
    def off(cls):
        return cls.OFF

    @classmethod
    def error(cls):
        return cls.BLOOD_RED
