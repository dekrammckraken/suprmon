class SignalColor:
    def __init__(self, r=0, g=0, b=0):
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
    def get_color_by_switch(cls, avail: bool):
        return cls.CREAM if avail else cls.BLOOD_RED

    @classmethod
    def unavail(cls):
        return cls.CHARCOAL

    @classmethod
    def off(cls):
        return cls.OFF

    @classmethod
    def error(cls):
        return cls.BLOOD_RED


# Palette (class attributes)
SignalColor.CHARCOAL = SignalColor(40, 40, 40)
SignalColor.BLOOD_RED = SignalColor(204, 36, 29)
SignalColor.OLIVE = SignalColor(152, 151, 26)
SignalColor.AMBER = SignalColor(215, 153, 33)
SignalColor.TEAL = SignalColor(69, 133, 136)
SignalColor.MAUVE = SignalColor(177, 98, 134)
SignalColor.MOSS = SignalColor(104, 157, 106)
SignalColor.TAUPE = SignalColor(168, 153, 132)
SignalColor.CLAY = SignalColor(146, 131, 116)
SignalColor.SCARLET = SignalColor(251, 73, 52)
SignalColor.LIME = SignalColor(184, 187, 38)
SignalColor.GOLD = SignalColor(250, 189, 47)
SignalColor.SEAFOAM = SignalColor(131, 165, 152)
SignalColor.ROSE = SignalColor(211, 134, 155)
SignalColor.MINT = SignalColor(142, 192, 124)
SignalColor.CREAM = SignalColor(235, 219, 178)
SignalColor.COAL = SignalColor(29, 32, 33)
SignalColor.OFF = SignalColor(0, 0, 0)
