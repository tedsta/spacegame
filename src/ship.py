#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.crew import Crew
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
        rooms = packet.read()
        crews = packet.read()
        for room_tuple in rooms: 
            self.add_room(*room_tuple)
        for crew_tuple in crews:
            crew = Crew(*crew_tuple)
            self.add_crew(crew, crew.position)

    def set_position(self, position):
        self.sprite.position = position
        for crew in self.crew:
            crew.sprite.position = self.sprite.position+self.room_offset+(crew.position*const.block_size)
        for room in self.rooms:
            room.sprite.position = self.sprite.position+sf.Vector2(room.position.x*const.block_size, room.position.y*const.block_size)+self.room_offset
    
    def add_room(self, room_type, x, y):
        width, height = const.room_dims[room_type]
        
        # Make sure there's space for the new room
        for i in range(x, x+width):
            for j in range(y, y+height):
                if self.room_grid.get(i, j): # Collides with existing room
                    return False
        
        # Create the room
        room = Room(room_type, x, y, width, height)
        room.sprite.position = self.sprite.position+sf.Vector2(x*const.block_size, y*const.block_size)+self.room_offset
        
        for i in range(x, x+width):
            for j in range(y, y+height):
                self.room_grid.set(i, j, room)
        
        self.rooms.append(room)
        return True
    
    def add_crew(self, crew, ship_position):
        # Make sure space is empty
        for c in self.crew:
            if c.position == ship_position:
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
