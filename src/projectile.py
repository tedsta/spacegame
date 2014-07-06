import sfml as sf

import src.res as res
from src.spritesheet import SpriteSheet

class Projectile:
    def __init__(self):
        self.sprite = SpriteSheet(res.blue_crew)
        self.sprite.init(1, 1)
        self.target_room = None
        self.start_position = sf.Vector2(0, 0)
        self.target_position = sf.Vector2(0, 0)
        self.fire_time = 0
        self.hit_time = 0
        self.hit = True # Hit or miss?
        self.active = False

    def apply_simulation_time(self, time):
        interp = (time - self.fire_time)/(self.hit_time - self.fire_time)
        self.sprite.position = self.start_position + (self.start_position - self.target_position)*interp
