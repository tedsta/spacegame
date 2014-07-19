from src.system import System
from src.weapon import Weapon

class WeaponSystem(System):
    def __init__(self, max_power=1):
        System.__init__(self)
        self.weapons = []
        self.power = 2
        self.max_power = 2

    def tuplify(self):
        return (1,)
