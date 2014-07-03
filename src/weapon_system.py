from src.system import System
from src.weapon import Weapon

class WeaponSystem(System):
    def __init__(self, weapons=None):
        System.__init__(self)
        if weapons:
            self.weapons = [Weapon(*w) for w in weapons]
        else:
            self.weapons = []

    def tuplify(self):
        return ([w.tuplify() for w in self.weapons],)
