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
        self.sprite = SpriteSheet(res.blue_crew)
        self.sprite.init(1, 1)
        self.path = []
        self.highlighted = False
        self.destination = None # Plan destination

        # Stats
        self.move_speed = 2 # Move speed in spaces per second

        # Crew interface stuff
        self.current_room = None
        self.target_room = None
    
    def set_highlighted(self, highlight):
        if highlight:
            self.sprite.texture = res.blue_crew_highlighted
        else:
            self.sprite.texture = res.blue_crew
        self.highlighted = highlight

    def apply_simulation_time(self, time):
        if not self.path: # Skip crew with no path
            return
        moves_completed = time*self.move_speed
        move_index = math.floor(moves_completed)
        move_interp = (moves_completed-move_index)
        if move_index+1 >= len(self.path): # Reached end of path
            position = sf.Vector2(*self.path[-1])
        else:
            start_pos = sf.Vector2(*self.path[move_index])
            end_pos = sf.Vector2(*self.path[move_index+1])
            position = start_pos + (end_pos-start_pos)*move_interp
        self.position = position

    def get_position_at_simulation_end(self):
        if not self.path:
            return self.position
        move_index = const.sim_time*self.move_speed
        return sf.Vector2(*self.path[min(len(self.path)-1, move_index)])

    def tuplify(self):
        return (self.id, self.position.x, self.position.y)
