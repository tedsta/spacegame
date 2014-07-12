import sfml as sf
import math

import src.res as res
from src.spritesheet import SpriteSheet

class Projectile:
    def __init__(self):
        self.sprite = SpriteSheet(res.laser_light1)
        self.sprite.init(4, 4)
        self.sprite.origin = self.sprite.frame_dim/2
        self.target_room = None
        self.start_position = sf.Vector2(0, 0)
        self.target_position = sf.Vector2(0, 0)
        self.fire_time = 0
        self.hit_time = 0
        self.hit = True # Hit or miss?
        self.active = False

    def apply_simulation_time(self, time):
        self.sprite.rotation = math.degrees(math.atan2(self.target_position.y-self.start_position.y, self.target_position.x-self.start_position.x))
        interp = (time - self.fire_time)/(self.hit_time - self.fire_time)
        self.sprite.position = self.start_position + (self.target_position-self.start_position)*interp
