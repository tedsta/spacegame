from src.system import System
from src.weapon import Weapon

class WeaponSystem(System):
    def __init__(self, max_power=1):
        System.__init__(self)
        self.weapons = []
        self.power = 0
        self.max_power = 3

    def on_power_changed(self):
        used = 0
        for weapon in self.weapons:
            if weapon.powered:
                if used+weapon.required_power <= self.get_max_usable_power():
                    used += weapon.required_power
                else:
                    weapon.powered = False

    def try_power_weapon(self, weapon):
        if self.get_max_usable_power()-self.power >= weapon.required_power:
            weapon.powered = True
            self.power += weapon.required_power
        else:
            weapon.powered = False
        return weapon.powered

    def depower_weapon(self, weapon):
        weapon.powered = False
        self.power -= weapon.required_power

    def tuplify(self):
        return (1,)
