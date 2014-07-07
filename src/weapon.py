import src.res as res
from src.spritesheet import SpriteSheet
from src.projectile import Projectile

class Weapon:
    def __init__(self, id):
        self.id = id
        self.sprite = SpriteSheet(res.weapon)
        self.sprite.init(1, 1)
        self.firing = False # Whether or not it's firing this turn
        self.powered = True # Is the weapon powered or unpowered
        self.target = None # Target room
        self.charge = 1
        self.required_charge = 1
        self.power = 1 # Power consumption
        self.projectile_type = None
        self.num_shots = 2

        self.projectiles = [Projectile(), Projectile()]
        
    def apply_simulation_time(self, time):
        for projectile in self.projectiles:
            if projectile.active:
                continue
            if time >= projectile.fire_time:
                projectile.active = True

    def tuplify(self):
        return (self.id, )
