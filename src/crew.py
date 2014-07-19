#!/usr/bin/env python

import sfml as sf
import math

import src.const as const
import src.res as res
from src.spritesheet import SpriteSheet

class Crew:

    def __init__(self, id=0, x=0, y=0):
        self.id = id
        self.position = sf.Vector2(x, y) # Position on ship grid
        self.sprite = SpriteSheet(res.human_base)
        self.sprite.init(117, 9)
        self.sprite.set_frame_loop(0, 0, False)
        self.highlight_sprite = SpriteSheet(res.human_color)
        self.highlight_sprite.init(117, 9)
        self.highlight_sprite.set_frame_loop(0, 0, False)
        self.highlight_sprite.color = sf.Color(0, 255, 0, 255)
        
        self.path = []
        self.highlighted = False
        self.destination = None # Plan destination
        self.health = 100
        self.max_health = 100

        # Stats
        self.move_speed = 2 # Move speed in spaces per second

        # Crew interface stuff
        self.current_room = None
        self.target_room = None
        
    def draw(self, target):
        if self.highlighted:
            self.highlight_sprite.position = self.sprite.position
            self.highlight_sprite.set_frame(self.sprite.frame)
            target.draw(self.highlight_sprite)
        #print(self.sprite.texture_rectangle.width, self.sprite.texture_rectangle.height)
        target.draw(self.sprite)
    
    def set_highlighted(self, highlight):
        self.highlighted = highlight

    def apply_simulation_time(self, time):
        if not self.path: # Skip crew with no path
            return
        moves_completed = time*self.move_speed
        move_index = math.floor(moves_completed)
        move_interp = (moves_completed-move_index)
        if move_index+1 >= len(self.path): # Reached end of path
            position = sf.Vector2(*self.path[-1])
            self.sprite.set_frame_loop(0, 0, False)
        else:
            start_pos = sf.Vector2(*self.path[move_index])
            end_pos = sf.Vector2(*self.path[move_index+1])
            direction = end_pos-start_pos
            position = start_pos + direction*move_interp
            
            # Do animations
            if direction.y == 1:
                self.sprite.set_frame_loop(0, 3)
            elif direction.y == -1:
                self.sprite.set_frame_loop(9, 12)
            elif direction.x == 1:
                self.sprite.set_frame_loop(4, 7)
            elif direction.x == -1:
                self.sprite.set_frame_loop(13, 16)
        self.position = position

    def get_position_at_simulation_end(self):
        if not self.path:
            return self.position
        move_index = const.sim_time*self.move_speed
        return sf.Vector2(*self.path[min(len(self.path)-1, move_index)])

    def tuplify(self):
        return (self.id, self.position.x, self.position.y)
