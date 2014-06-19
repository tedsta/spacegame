#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.room import Room

class Ship:

    def __init__(self):
        self._sprite = sf.Sprite(res.ship)
        self._room_offset = sf.Vector2(35, 10) # Offset of room origin
        
        # Room stuff
        self._rooms = []
        self._room_grid = Grid(10, 10)
        
        # Crew stuff
        self._crew = []

    def serialize(self, packet):
        packet.write([room.tuplify() for room in self._rooms])
        packet.write([crew.tuplify() for crew in self._crew])

    def deserialize(self, packet):
        self._rooms = [Room(*room) for room in packet.read()]
        self._crew = [Crew(*crew) for crew in packet.read()]
    
    def add_room(self, room_type, x, y):
        width, height = const.room_dims[const.room2x2]
        
        # Make sure there's space for the new room
        for i in range(x, x+width):
            for j in range(y, y+height):
                if self._room_grid.get(i, j): # Collides with existing room
                    return False
        
        # Create the room
        room = Room(room_type, x, y, width, height)
        room.sprite.position = sf.Vector2(x*const.block_size, y*const.block_size)+self._room_offset
        
        for j in range(x, x+width):
            for j in range(y, y+height):
                self._room_grid.set(i, j, room)
        
        self._rooms.append(room)
        return True
    
    def add_crew(self, crew, ship_position):
        # Make sure space is empty
        for crew in self._crew:
            if crew.position == ship_position:
                return False
        # Make sure the space is a room
        if not self._room_grid.get(ship_position.x, ship_position.y):
            return False
        # All is well, add the member
        self._crew.append(crew)
        crew.position = ship_position
        crew.sprite.position = self._sprite.position+self._room_offset+(ship_position*const.block_size)
        return True
    
    def draw(self, target):
        target.draw(self._sprite)
        for room in self._rooms:
            target.draw(room.sprite)
        for crew in self._crew:
            target.draw(crew.sprite)
