class SignalColor:
    def __init__(self, r,g,b):
        self.r = r
        self.g = g
        self.b = b
    
    def to_hex(self):
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"