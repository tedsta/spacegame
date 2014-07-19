#!/usr/bin/env python

import sfml as sf
import src.const as const
import src.res as res
from src.spritesheet import SpriteSheet

class Room:

    def __init__(self, room_type, x, y, id=''):
        self.id = id
        self.ship = None # The ship that this room belongs to
        self.system = None # The system this room is associated with
        self.room_type = room_type
        self.position = sf.Vector2(x, y)
        self.width, self.height = const.room_dims[room_type]

        self.sprite = sf.Sprite(res.room_textures[room_type])
        if res.room_overlays[room_type]:
            self.overlay_sprite = sf.Sprite(res.room_overlays[room_type])
        else:
            self.overlay_sprite = None
        if res.room_icons[room_type]:
            self.icon_sprite = sf.Sprite(res.room_icons[room_type])
            self.icon_sprite.origin = self.icon_sprite.local_bounds.size/2
        else:
            self.icon_sprite = None

        # Crew coordination stuff
        self.free_positions = [sf.Vector2(x+i, y+j) for j in reversed(range(0, self.height)) for i in reversed(range(0, self.width))]

    def set_position(self, position):
        self.sprite.position = position
        if self.overlay_sprite:
            self.overlay_sprite.position = position
        if self.icon_sprite:
            self.icon_sprite.position = position+(self.sprite.global_bounds.size/2)

    def update_sprites(self, dt):
        if self.system:
            if self.system.damage == 0:
                self.icon_sprite.color = sf.Color(120, 120, 120, 255)
            elif self.system.damage < self.system.max_power:
                self.icon_sprite.color = sf.Color(200, 200, 50, 255)
            elif self.system.damage == self.system.max_power:
                self.icon_sprite.color = sf.Color(255, 0, 0, 255)

    def draw(self, target):
        target.draw(self.sprite)
        if self.overlay_sprite:
            target.draw(self.overlay_sprite)
        if self.icon_sprite:
            target.draw(self.icon_sprite)
    
    def is_full(self):
        return len(self.free_positions) == 0
    
    def get_free_position(self):
        return self.free_positions.pop()

    def take_position(self, position):
        if position in self.free_positions:
            self.free_positions.remove(position)
            return True
        return False

    def freeup_position(self, position):
        rect = sf.Rectangle(self.position, sf.Vector2(self.width, self.height))
        if rect.contains(position) and position not in self.free_positions:
            self.free_positions.append(position)

    def tuplify(self):
        return (self.room_type, self.position.x, self.position.y, self.id)
