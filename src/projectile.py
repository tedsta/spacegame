import sfml as sf
import math

import src.res as res
from src.spritesheet import SpriteSheet

class Projectile:
    def __init__(self):
        self.sprite = SpriteSheet(res.laser_light1)
        self.sprite.init(4, 4)
        self.sprite.origin = self.sprite.frame_dim/2
        self.explosion_sprite = SpriteSheet(res.explosion_missile1)
        self.explosion_sprite.init(9, 9, 0.05)
        self.explosion_sprite.origin = self.explosion_sprite.frame_dim/2
        self.damage = 1
        self.phase = 0 # 0 = Weapon to offscreen, 1 = offscreen to target, 2 = detonation
        self.target_room = None
        self.start_position = sf.Vector2(0, 0)
        self.to_offscreen_position = sf.Vector2(0, 0)
        self.from_offscreen_position = sf.Vector2(0, 0)
        self.target_position = sf.Vector2(0, 0)
        self.fire_time = 0
        self.hit_time = 0
        self.hit = True # Hit or miss?
        self.active = False
        self.is_mine = False # Does this projectile belong to me? (Client only, used for lock_window stuff)

    def apply_simulation_time(self, time):
        if self.phase == 0:
            start_position = self.start_position
            end_position = self.to_offscreen_position
            interp = (time - self.fire_time)/(1.0) # Half a second to offscreen
            if time > self.fire_time+1.0:
                self.phase = 1
        elif self.phase == 1:
            start_position = self.from_offscreen_position
            end_position = self.target_position
            interp = (time - (self.hit_time-0.7))/(0.7) # Third of a second from offscreen to target
            #if time > self.hit_time:
            #    self.phase = 2
            
        self.sprite.rotation = math.degrees(math.atan2(end_position.y-start_position.y, end_position.x-start_position.x))
        self.sprite.position = start_position + (end_position-start_position)*interp

    def detonate(self):
        self.target_room.ship.hull_points -= self.damage
        if self.target_room.system:
            self.target_room.system.deal_damage(self.damage)
        self.active = False
        self.phase = 2
        self.explosion_sprite.set_frame_loop(0, 8, False)
        self.explosion_sprite.position = self.sprite.position
