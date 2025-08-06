from signalcolor import SignalColor

MAX_LED = 5


class SuprSignal:
    def __init__(self, sensor, color: SignalColor) -> str:
        row,col = sensor
        self.index = (row - 1) * MAX_LED + col
        self.color = color

    def compose(self):
        return f"{self.index:02d}x{self.color.to_hex()}"
