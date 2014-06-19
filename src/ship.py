#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.room import Room

class Ship:

    def __init__(self):
        self.sprite = sf.Sprite(res.ship)
        self.room_offset = sf.Vector2(35, 10) # Offset of room origin
        
        # Room stuff
        self.rooms = []
        self.room_grid = Grid(10, 10)
        
        # Crew stuff
        self.crew = []

    def serialize(self, packet):
        packet.write([room.tuplify() for room in self.rooms])
        packet.write([crew.tuplify() for crew in self.crew])

    def deserialize(self, packet):
        self.rooms = [Room(*room) for room in packet.read()]
        self.crew = [Crew(*crew) for crew in packet.read()]
    
    def add_room(self, room_type, x, y):
        width, height = const.room_dims[const.room2x2]
        
        # Make sure there's space for the new room
        for i in range(x, x+width):
            for j in range(y, y+height):
                if self.room_grid.get(i, j): # Collides with existing room
                    return False
        
        # Create the room
        room = Room(room_type, x, y, width, height)
        room.sprite.position = sf.Vector2(x*const.block_size, y*const.block_size)+self.room_offset
        
        for j in range(x, x+width):
            for j in range(y, y+height):
                self.room_grid.set(i, j, room)
        
        self.rooms.append(room)
        return True
    
    def add_crew(self, crew, ship_position):
        # Make sure space is empty
        for crew in self.crew:
            if crew.position == ship_position:
                return False
        # Make sure the space is a room
        if not self.room_grid.get(ship_position.x, ship_position.y):
            return False
        # All is well, add the member
        self.crew.append(crew)
        crew.position = ship_position
        crew.sprite.position = self.sprite.position+self.room_offset+(ship_position*const.block_size)
        return True
    
    def draw(self, target):
        target.draw(self.sprite)
        for room in self.rooms:
            target.draw(room.sprite)
        for crew in self.crew:
            target.draw(crew.sprite)
