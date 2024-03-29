import sfml as sf

import src.res as res
from src.spritesheet import SpriteSheet
from src.projectile import Projectile

class Weapon:
    def __init__(self, id):
        self.id = id
        self.sprite = SpriteSheet(res.weapon)
        self.sprite.init(12, 12, 0.06)
        self.sprite.set_frame_loop(5, 5, False)

        self.slot = None # WeaponSlot this weapon is in
        self.position = sf.Vector2(0, 0)

        self.firing = False # Whether or not it's firing this turn
        self.powered = False # Is the weapon powered or unpowered
        self.was_powered = False # Was the weapon powered last turn? (Used for weapon slide out/in animation)
        self.target = None # Target room

        self.charge = 0

        self.required_charge = 1
        self.required_power = 1 # Power consumption
        self.projectile_type = None
        self.num_shots = 2

        self.projectiles = [Projectile(), Projectile()]
        
    def apply_simulation_time(self, time):
        if time <= 0.3: # weapon slide in/out animation
            if self.powered and not self.was_powered:
                self.position = self.slot.position + self.slot.powered_offset*(time/0.3)
            if not self.powered and self.was_powered:
                self.position = self.slot.position+self.slot.powered_offset - self.slot.powered_offset*(time/0.3)
    
        if self.firing:
            for projectile in self.projectiles:
                if time >= projectile.fire_time:
                    if time <= projectile.hit_time:
                        if not projectile.active:
                            self.sprite.set_frame_loop(5, 11, False)
                        projectile.active = True
                    else:
                        if projectile.hit and projectile.active:
                            projectile.detonate()

    def tuplify(self):
        return (self.id, )
