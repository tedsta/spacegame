#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.room import Room

class Ship:

    def __init__(self):
        self._back = sf.Sprite(res.ship)
        self._room_offset = sf.Vector2(35, 10) # Offset of room origin
        self._rooms = []
        self._room_grid = Grid(10, 10)
    
    def add_room(self, room_type, x, y):
        width, height = const.room_dims[const.room2x2]
        
        # Make sure there's space for the new room
        for i in range(x, x+width):
            for j in range(y, y+height):
                if self._room_grid.get(i, j): # Collides with existing room
                    return False
        
        # Create the room
        room = Room(room_type, x, y, width, height, res.room_textures[const.room2x2])
        room.sprite.position = sf.Vector2(x*const.block_size, y*const.block_size)+self._room_offset
        
        for j in range(x, x+width):
            for j in range(y, y+height):
                self._room_grid.set(i, j, room)
        
        self._rooms.append(room)
        return True
    
    def draw(self, target):
        target.draw(self._back)
        for room in self._rooms:
            target.draw(room.sprite)