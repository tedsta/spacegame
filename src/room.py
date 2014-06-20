#!/usr/bin/env python

import sfml as sf
import src.res as res

class Room:

    def __init__(self, room_type, x, y, width, height):
        self.room_type = room_type
        self.position = sf.Vector2(x, y)
        self.width = width
        self.height = height
        self.sprite = sf.Sprite(res.room_textures[room_type])
    
    def is_full(self):
        return False
    
    def get_free_position(self):
        return self.position

    def tuplify(self):
        return (self.room_type, self.position.x, self.position.y)
