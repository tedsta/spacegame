#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.crew import Crew
from src.room import Room
from src.door import Door
from src.path import WalkDirs

from src.weapon import Weapon
from src.weapon_system import WeaponSystem
from src.engine_system import EngineSystem

class WeaponSlot:
    def __init__(self, x, y, rotate, mirror, slide_dir, weapon_tup=None):
        self.position = sf.Vector2(x, y)

        # Rotation
        if rotate:
            self.rotation = 90
        else:
            self.rotation = 0

        # Mirror?
        self.scale = sf.Vector2(1, 1)
        if mirror:
            if rotate:
                self.scale.x = -1
            else:
                self.scale.y = -1

        # Handle direction
        self.slide_dir = slide_dir
        if slide_dir == "left":
            self.powered_offset = sf.Vector2(-15, 0)
        elif slide_dir == "right":
            self.powered_offset = sf.Vector2(15, 0)
        elif slide_dir == "up":
            self.powered_offset = sf.Vector2(0, -5)
        elif slide_dir == "down":
            self.powered_offset = sf.Vector2(0, 5)

        self.rotate = rotate
        self.mirror = mirror

        if weapon_tup:
            self.weapon = Weapon(*weapon_tup)
            self.weapon.slot = self
            self.weapon.position = self.position
        else:
            self.weapon = None

    def tuplify(self):
        if self.weapon:
            return (self.position.x, self.position.y, self.rotate, self.mirror, self.slide_dir, self.weapon.tuplify())
        else:
            return (self.position.x, self.position.y, self.rotate, self.mirror, self.slide_dir)

class Ship:

    def __init__(self, id=""):
        self.id = id

        # Drawing stuff
        self.sprite = sf.Sprite(res.ship)
        self.sprite_offset = sf.Vector2(-71, -40)
        self.room_offset = sf.Vector2(63, 32) # Offset of room origin
        self.position = sf.Vector2(0, 0)

        # Stats n stuff
        self.alive = True
        self.exploding = False # Playing the explosion animation
        self.hull_points = 10

        # Path grid for pathfinding
        self.path_grid = Grid(10, 10)
        
        # Things on the ship
        self.rooms = []
        self.doors = []
        self.crew = []

        self.weapon_slots = []
        
        self.weapon_system = None
        self.engine_system = EngineSystem()

    def serialize(self, packet):
        packet.write(self.id)
        packet.write([slot.tuplify() for slot in self.weapon_slots])
        if self.weapon_system:
            packet.write(self.weapon_system.tuplify())
        else:
            packet.write(None)
        packet.write([room.tuplify() for room in self.rooms])
        packet.write([crew.tuplify() for crew in self.crew])

    def deserialize(self, packet):
        self.id = packet.read()
        # Weapon slots
        weapon_slots = packet.read()
        for slot in weapon_slots:
            self.weapon_slots.append(WeaponSlot(*slot))
        # Weapon system
        weap_sys_tuple = packet.read()
        if weap_sys_tuple:
            self.weapon_system = WeaponSystem(*weap_sys_tuple)
            for slot in self.weapon_slots:
                if slot.weapon:
                    self.weapon_system.weapons.append(slot.weapon)
        rooms = packet.read()
        for room_tuple in rooms: 
            self.add_room(*room_tuple)
        crews = packet.read()
        for crew_tuple in crews:
            crew = Crew(*crew_tuple)
            self.add_crew(crew, crew.position.x, crew.position.y)

    def set_position(self, position):
        self.position = position
    
    def add_room(self, room_type, x, y, id=''):
        if not id:
            id = self.id+"room:"+str(len(self.rooms))
        # Create the room
        room = Room(room_type, x, y, id)
        room.ship = self
        room.sprite.position = self.sprite.position+sf.Vector2(x*const.block_size, y*const.block_size)+self.room_offset

        width, height = room.width, room.height
        
        # Make sure there's space for the new room
        if self.room_at(x, y, width, height):
            return False

        # Add doors
        # X axis
        for i in range(x, x+width):
            # Top side
            if self.room_at(i, y-1):
                self.add_door(sf.Vector2(i, y-1), sf.Vector2(i, y))
            # Bottom side
            if self.room_at(i, y+height):
                self.add_door(sf.Vector2(i, y+height-1), sf.Vector2(i, y+height))
        # Y axis
        for j in range(y, y+height):
            # Left side
            if self.room_at(x-1, j):
                self.add_door(sf.Vector2(x-1, j), sf.Vector2(x, j))
            # Right side
            if self.room_at(x+width, j):
                self.add_door(sf.Vector2(x+width-1, j), sf.Vector2(x+width, j))

        # Link room to system
        if room_type == const.room_engines2x2:
            room.system = self.engine_system
        elif room_type == const.room_weapons2x2:
            room.system = self.weapon_system

        # Update sprites
        room.update_sprites(0)
        
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
    
    def add_crew(self, crew, x, y):
        position = sf.Vector2(x, y)
    
        # Make sure the space is a room
        room = self.room_at(x, y)
        if not room:
            return False
        # Take position from room free positions
        if not room.take_position(position):
            # If the space isn't free, the crew can't be added there
            return False
        crew.current_room = room # For the crew interface
        # All is well, add the member
        crew.position = position
        crew.sprite.position = self.sprite.position+self.room_offset+(position*const.block_size)
        self.crew.append(crew)
        return True

    def add_weapon_slot(self, x, y, rotate, mirror, slide_dir):
        self.weapon_slots.append(WeaponSlot(x, y, rotate, mirror, slide_dir))

    def add_weapon(self, weapon):
        for slot in self.weapon_slots:
            # Find empty slot
            if not slot.weapon:
                slot.weapon = weapon
                weapon.slot = slot
                weapon.position = slot.position
                # Just to make sure it's not powered
                weapon.was_powered = False
                weapon.powered = False
                # Add it to the weapon system
                self.weapon_system.weapons.append(weapon)
                return True
        return False
    
    def room_at(self, x, y, w=1, h=1):
        for room in self.rooms:
            # Check for room collision
            if x < room.position.x+room.width and x+w > room.position.x and\
               y < room.position.y+room.height and y+h > room.position.y:
                return room
        return None

    def blow_up(self):
        self.alive = False
        self.exploding = True

    def update_sprites(self, dt):
        if self.alive:
            # First, update all the sprite positions
            for crew in self.crew:
                crew.sprite.update(dt)
            for room in self.rooms:
                room.update_sprites(dt)
            if self.weapon_system:
                for weapon in self.weapon_system.weapons:
                    weapon.sprite.update(dt)
            for door in self.doors:
                door.sprite.update(dt)
        else:
            self.exploding = False
    
    def draw_hull_points(self, target):
        for i in range(0, self.hull_points):
            res.ship_hull_point_rect.position = self.position + sf.Vector2(2 + i*16, -50)
            target.draw(res.ship_hull_point_rect)
    
    def draw(self, target):
        # First, update all the sprite positions
        self.sprite.position = self.position+self.sprite_offset
        for crew in self.crew:
            crew.sprite.position = self.sprite.position+self.room_offset+(crew.position*const.block_size)
        for room in self.rooms:
            room.set_position(self.sprite.position+sf.Vector2(room.position.x*const.block_size, room.position.y*const.block_size)+self.room_offset)
        if self.weapon_system:
            for weapon in self.weapon_system.weapons:
                weapon.sprite.origin = weapon.sprite.frame_dim/2
                weapon.sprite.position = self.sprite.position+weapon.position
                if weapon.slot.rotate:
                    weapon.sprite.rotation = weapon.slot.rotation
                if weapon.slot.mirror:
                    weapon.sprite.ratio = weapon.slot.scale
        for door in self.doors:
            # Horizontal
            if door.pos_b-door.pos_a == sf.Vector2(1, 0):
                door.sprite.position = self.sprite.position+self.room_offset+(door.pos_b*const.block_size)+sf.Vector2(-3, 7)
            # Vertical
            elif door.pos_b-door.pos_a == sf.Vector2(0, 1):
                door.sprite.position = self.sprite.position+self.room_offset+(door.pos_b*const.block_size)+sf.Vector2(7, -3)

        if self.alive:
            # Draw everything
            if self.weapon_system:
                for weapon in self.weapon_system.weapons:
                    target.draw(weapon.sprite)
            target.draw(self.sprite)
            for room in self.rooms:
                room.draw(target)
            for door in self.doors:
                target.draw(door.sprite)
            for crew in self.crew:
                crew.draw(target)
                # Draw crew health bar
                health_bar = sf.RectangleShape()
                health_bar.position = sf.Vector2(crew.sprite.position.x+7, crew.sprite.position.y-2)
                ratio = crew.health/crew.max_health
                health_bar.size = sf.Vector2(20*ratio, 5)
                health_bar.fill_color = sf.Color.GREEN
                target.draw(health_bar)
        elif self.exploding:
            pass

    ###################################
    # Helper stuff

    def _rebuild_path_grid(self):
        # Clear path grid
        self.path_grid.fill(WalkDirs())

        # Setup rooms' walkable area (rooms don't connect yet)
        for room in self.rooms:
            x = room.position.x
            y = room.position.y
            width = room.width
            height = room.height
            # General case, 2d room
            if width > 1 and height > 1:
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
                    print("x")
                    # Top side
                    self.path_grid.set(i, y, WalkDirs(left=True, down_left=True, right=True, down_right=True, down=True))
                    # Bottom side
                    self.path_grid.set(i, y+height-1, WalkDirs(left=True, up_left=True, right=True, up_right=True, up=True))
                # Y axis
                for j in range(y+1, y+height-1):
                    print("y")
                    # Left side
                    self.path_grid.set(x, j, WalkDirs(up=True, up_right=True, down=True, down_right=True, right=True))
                    # Right side
                    self.path_grid.set(x+width-1, j, WalkDirs(up=True, up_left=True, down=True, down_left=True, left=True))
                ### Internals
                for i in range(x+1, x+width-1):
                    for j in range(y+1, y+height-1):
                        self.path_grid.set(i, j, WalkDirs(up_left=True, up=True, up_right=True, left=True, right=True, down_left=True, down=True, down_right=True))
            elif height == 1: # Special case: horizontal room
                # Left
                self.path_grid.set(x, y, WalkDirs(right=True))
                # Right
                self.path_grid.set(x+width-1, y, WalkDirs(left=True))
                # Inbetween
                for i in range(x+1, x+width-1):
                    self.path_grid.set(i, y, WalkDirs(left=True, right=True))
            elif width == 1: # Special case: vertical room
                # Left
                self.path_grid.set(x, y, WalkDirs(down=True))
                # Right
                self.path_grid.set(x, y+height-1, WalkDirs(up=True))
                # Inbetween
                for j in range(y+1, y+height-1):
                    self.path_grid.set(x, j, WalkDirs(down=True, up=True))
        
        # Connect rooms with doors
        for door in self.doors:
            # Horizontal
            if door.pos_b-door.pos_a == sf.Vector2(1, 0):
                self.path_grid.get(door.pos_a.x, door.pos_a.y).right = True
                self.path_grid.get(door.pos_b.x, door.pos_b.y).left = True
            # Vertical
            elif door.pos_b-door.pos_a == sf.Vector2(0, 1):
                self.path_grid.get(door.pos_a.x, door.pos_a.y).down = True
                self.path_grid.get(door.pos_b.x, door.pos_b.y).up = True
