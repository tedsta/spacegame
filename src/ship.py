#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.crew import Crew
from src.room import Room
from src.door import Door
from src.path_finding import WalkDirs

class Ship:

    def __init__(self):
        self.sprite = sf.Sprite(res.ship)
        self.room_offset = sf.Vector2(35, 10) # Offset of room origin

        # Path grid for pathfinding
        self.path_grid = Grid(10, 10)
        
        # Room stuff
        self.rooms = []
        self.doors = []
        
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
        for door in self.doors:
            # Horizontal
            if door.pos_b-door.pos_a == sf.Vector2(1, 0):
                door.sprite.position = self.sprite.position+self.room_offset+(door.pos_b*const.block_size)+sf.Vector2(-3, 7)
            # Vertical
            elif door.pos_b-door.pos_a == sf.Vector2(0, 1):
                door.sprite.position = self.sprite.position+self.room_offset+(door.pos_b*const.block_size)+sf.Vector2(7, -3)
    
    def add_room(self, room_type, x, y):
        width, height = const.room_dims[room_type]
        
        # Make sure there's space for the new room
        if self._room_at(x, y, width, height):
            return False
        
        # Create the room
        room = Room(room_type, x, y, width, height)
        room.sprite.position = self.sprite.position+sf.Vector2(x*const.block_size, y*const.block_size)+self.room_offset

        # Add doors
        # X axis
        for i in range(x, x+width):
            # Top side
            if self._room_at(i, y-1):
                self.add_door(sf.Vector2(i, y-1), sf.Vector2(i, y))
            # Bottom side
            if self._room_at(i, y+height):
                self.add_door(sf.Vector2(i, y+height-1), sf.Vector2(i, y+height))
        # Y axis
        for j in range(y, y+height):
            # Left side
            if self._room_at(x-1, j):
                self.add_door(sf.Vector2(x-1, j), sf.Vector2(x, j))
            # Right side
            if self._room_at(x+width, j):
                self.add_door(sf.Vector2(x+width-1, j), sf.Vector2(x+width, j))
        
        self.rooms.append(room)
        self._rebuild_path_grid()
        return True

    def add_door(self, pos_a, pos_b):
        door = Door(pos_a, pos_b)
        # Horizontal
        if pos_b-pos_a == sf.Vector2(1, 0):
            door.sprite.position = self.sprite.position+self.room_offset+(pos_b*const.block_size)+sf.Vector2(-3, 7)
        # Vertical
        elif pos_b-pos_a == sf.Vector2(0, 1):
            door.sprite.position = self.sprite.position+self.room_offset+(pos_b*const.block_size)+sf.Vector2(7, -3)
        # WTF?
        else:
            return False
        self.doors.append(door)
        return True
    
    def add_crew(self, crew, ship_position):
        # Make sure space is empty
        for c in self.crew:
            if c.position == ship_position:
                return False
        # Make sure the space is a room
        if not self._room_at(ship_position.x, ship_position.y):
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
        for door in self.doors:
            target.draw(door.sprite)
        for crew in self.crew:
            target.draw(crew.sprite)

    ###################################
    # Helper stuff

    def _room_at(self, x, y, w=1, h=1):
        for room in self.rooms:
            # Check for room collision
            if x < room.position.x+room.width and x+w > room.position.x and\
               y < room.position.y+room.height and y+h > room.position.y:
                return True
        return False

    def _rebuild_path_grid(self):
        # Clear path grid
        self.path_grid.fill(WalkDir())

        # Setup rooms' walkable area (rooms don't connect yet)
        for room in self.rooms:
            x = room.position.x
            y = room.position.y
            width = room.width
            height = room.height
            ### Corners
            # Top left
            self.path_grid.set(x, y, WalkDirs(down=True, right=True, down_right=True))
            # Top right
            self.path_grid.set(x+width-1, y, WalkDirs(down=True, left=True, down_left=True))
            # Bottom left
            self.path_grid.set(x, y+height-1, WalkDirs(up=True, right=True, up_right=True))
            # Bottom right
            self.path_grid.set(x+width-1, y+height-1, WalkDirs(up=True, left=True, up_left=True))
            ### Edges
            # X axis
            for i in range(x+1, x+width-1):
                # Top side
                self.path_grid.set(i, y, WalkDirs(left=True, down_left=True, right=True, down_right=True, down=True))
                # Bottom side
                self.path_grid.set(i, y+height-1, WalkDirs(left=True, up_left=True, right=True, up_right=True, up=True))
            # Y axis
            for j in range(y+1, y+height-1):
                # Left side
                self.path_grid.set(x, j, WalkDirs(up=True, up_right=True, down=True, down_right=True, right=True))
                # Right side
                self.path_grid.set(x+width-1, j, WalkDirs(up=True, up_left=True, down=True, down_left=True, left=True))
            ### Internals
            for i in range(x+1, x+width-1):
                for j in range(y+1, y+height-1):
                    self.path_grid.set(i, j, WalkDirs(up_left=True, up=True, up_right=True, left=True, right=True, down_left=True, down=True, down_right=True))
        
        # Connect rooms with doors
        for door in self.doors:
            # Horizontal
            if door.pos_b-door.pos_a == sf.Vector2(1, 0):
                self.path_grid.get(door.pos_a.x, door.pos_a.y).right = True
                self.path_grid.get(door.pos_b.x, door.pos_b.y).left = True
            # Vertical
            elif door.pos_b-door.pos_a == sf.Vector2(0, 1):
                self.path_grid.get(door.pos_a.x, door.pos_a.y).down = True
                self.path_grid.get(door.pos_b.x, door.pos_b.y).left = True
