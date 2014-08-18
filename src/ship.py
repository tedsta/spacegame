#!/usr/bin/env python

import math
import random
import sfml as sf

import src.res as res
import src.const as const
from src.grid import Grid
from src.room import Room
from src.door import Door

from src.weapon import Weapon
from src.weapon_system import WeaponSystem
from src.shield_system import ShieldSystem
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

class HullPiece:
    
    def __init__(self, texture, position, speed_min, speed_max, dir_min, dir_max, ang_min, ang_max):
        self.sprite = sf.Sprite(texture)
        self.sprite.origin = self.sprite.local_bounds.size/2
        
        self.position = self.sprite.origin+position
        self.speed_min = speed_min
        self.speed_max = speed_max
        self.dir_min = dir_min
        self.dir_max = dir_max
        self.ang_min = ang_min
        self.ang_max = ang_max
        
        self.velocity = sf.Vector2(math.cos(math.radians(dir_min)), math.sin(math.radians(dir_min)))*speed_min
        self.angular_velocity = ang_min
        
    def apply_time(self, ship, time):
        self.sprite.position = ship.sprite.position+self.position+(self.velocity*time)
        self.sprite.rotation = ship.sprite.rotation+(self.angular_velocity*time)

class Ship:

    def __init__(self, id=""):
        self.id = id

        # Drawing stuff
        self.sprite = sf.Sprite(res.ship)
        self.sprite_offset = sf.Vector2(-71, -40)
        self.room_offset = sf.Vector2(63, 32) # Offset of room origin
        self.position = sf.Vector2(0, 0)
        
        # Shield renering
        self.shields_offset = sf.Vector2(-30, -50)
        self.shields_sprite = sf.Sprite(res.shields)
        #self.shields_sprite.origin - self.shields_sprite.local_bounds.size/2

        # Stats n stuff
        self.alive = True
        self.hull_points = 10
        
        # Explosion stuff
        self.exploding = False # Playing the explosion animation
        self.explosion_timer = 0
        
        self.hull_pieces = [\
        HullPiece(res.ship_piece1, sf.Vector2(205, 60), 10, 20, 0, 360, -30, 30),\
        HullPiece(res.ship_piece2, sf.Vector2(70, 108), 20, 40, 160, 200, -40, 40),\
        HullPiece(res.ship_piece3, sf.Vector2(130, 127), 40, 60, 220, 260, -60, -20),\
        HullPiece(res.ship_piece4, sf.Vector2(17, 0), 30, 50, 20, 70, -30, 30),\
        HullPiece(res.ship_piece5, sf.Vector2(0, 61), 40, 80, 110, 160, -30, 30),\
        HullPiece(res.ship_piece6, sf.Vector2(72, 0), 20, 50, 330, 350, -30, 30),\
        ]

        # Path grid for pathfinding
        self.path_grid = Grid(10, 10)
        
        # Things on the ship
        self.rooms = []
        self.doors = []

        self.weapon_slots = []
        
        self.weapon_system = None
        self.engine_system = EngineSystem()
        self.shield_system = None

    def serialize(self, packet):
        packet.write(self.id)
        packet.write([slot.tuplify() for slot in self.weapon_slots])
        if self.weapon_system:
            packet.write(self.weapon_system.tuplify())
        else:
            packet.write(None)
        if self.shield_system:
            packet.write(self.shield_system.tuplify())
        else:
            packet.write(None)
        packet.write([room.tuplify() for room in self.rooms])

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
        # Shield system
        shield_sys_tuple = packet.read()
        if shield_sys_tuple:
            self.shield_system = ShieldSystem(*shield_sys_tuple)
        rooms = packet.read()
        for room_tuple in rooms: 
            self.add_room(*room_tuple)

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
        elif room_type == const.room_shields2x2:
            room.system = self.shield_system

        # Update sprites
        room.update_sprites(0)
        
        self.rooms.append(room)
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
        self.explosion_timer = 0
        
        # Randomize pieces' trajectories
        for piece in self.hull_pieces:
            speed = random.uniform(piece.speed_min, piece.speed_max)
            dir = random.uniform(piece.dir_min, piece.dir_max)
            ang = random.uniform(piece.ang_min, piece.ang_max)
        
            piece.velocity = sf.Vector2(math.cos(math.radians(dir)), math.sin(math.radians(dir))) * speed
            piece.angular_velocity = ang

    def update_sprites(self, dt):
        if self.alive:
            # First, update all the sprite positions
            for room in self.rooms:
                room.update_sprites(dt)
            if self.weapon_system:
                for weapon in self.weapon_system.weapons:
                    weapon.sprite.update(dt)
            for door in self.doors:
                door.sprite.update(dt)
        elif self.exploding:
            self.explosion_timer += dt
            for piece in self.hull_pieces:
                piece.apply_time(self, self.explosion_timer)
    
    def draw_hull_points(self, target):
        for i in range(0, self.hull_points):
            res.ship_hull_point_rect.position = self.position + sf.Vector2(2 + i*16, -80)
            target.draw(res.ship_hull_point_rect)
        if self.shield_system:
            for i in range(0, self.shield_system.shields):
                res.ship_shield_point_rect.position = self.position + sf.Vector2(2 + i*16, -50)
                target.draw(res.ship_shield_point_rect)
    
    def draw(self, target):
        # First, update all the sprite positions
        self.sprite.position = self.position+self.sprite_offset
        self.shields_sprite.position = self.position+self.sprite_offset+self.shields_offset
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
            if self.shield_system:
                self.shields_sprite.color = sf.Color(255, 255, 255, self.shield_system.shields * (255//4))
                target.draw(self.shields_sprite)
            if self.weapon_system:
                for weapon in self.weapon_system.weapons:
                    target.draw(weapon.sprite)
            target.draw(self.sprite)
            for room in self.rooms:
                room.draw(target)
            for door in self.doors:
                target.draw(door.sprite)
        elif self.exploding:
            for piece in self.hull_pieces:
                target.draw(piece.sprite)
