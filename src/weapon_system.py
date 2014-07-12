from src.system import System
from src.weapon import Weapon

class WeaponSystem(System):
    def __init__(self, max_power=1):
        System.__init__(self)
        self.weapons = []

    def tuplify(self):
        return (1,)
