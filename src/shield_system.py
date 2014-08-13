from src.system import System

class ShieldSystem(System):
    def __init__(self, max_power=8):
        System.__init__(self)
        self.power = max_power
        self.max_power = max_power
        
        self.shields = self.power//2
        self.max_shields = self.power//2

    def on_power_changed(self):
        self.max_shields = self.power//2
        self.shields = min(self.shields, self.max_shields)

    def tuplify(self):
        return (self.max_power,)
