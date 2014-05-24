#!/usr/bin/env python

import sfml as sf

import src.res as res
from src.grid import Grid
from src.room import Room

class Ship:

    def __init__(self):
        self._back = sf.Sprite(res.ship)
        self._room_offset = sf.Vector2(35, 10) # Offset of room origin
        self._rooms = []
        self._room_grid = Grid(10, 10)
    
    def add_room(self, room_type, x, y):
        width, height = res.room_dims[res.room2x2]
        
        room = Room(room_type, x, y, width, height, res.room_textures[res.room2x2])
        room.sprite.position = sf.Vector2(x*res.block_size, y*res.block_size)+self._room_offset
        
        for x in range(x, width):
            for y in range(y, height):
                self._room_grid.set(x, y, room)
        
        self._rooms.append(room)
    
    def draw(self, target):
        target.draw(self._back)
        for room in self._rooms:
            target.draw(room.sprite)