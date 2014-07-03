import src.res as res
from src.projectile import Projectile

class Weapon:
    def __init__(self, id):
        self.id = id
        self.sprite = res.weapon
        self.active = False
        self.target = None # Target room
        self.charge = 0
        self.required_charge = 1
        self.power = 1 # Power consumption
        self.projectile_type = None
        self.num_shots = 2

        self.projectiles = [Projectile(), Projectile()]

    def tuplify(self):
        return (self.id, )
