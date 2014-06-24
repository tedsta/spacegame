#!/usr/bin/env python

import sfml as sf
import src.const as const
import src.res as res

class Room:

    def __init__(self, room_type, x, y):
        self.room_type = room_type
        self.position = sf.Vector2(x, y)
        self.width, self.height = const.room_dims[room_type]
        self.sprite = sf.Sprite(res.room_textures[room_type])

        # Crew coordination stuff
        self.free_positions = [sf.Vector2(x+i, y+j) for i in range(0, self.width) for j in range(0, self.height)]
    
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
        return (self.room_type, self.position.x, self.position.y)
