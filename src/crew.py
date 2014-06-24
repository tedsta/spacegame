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

    def get_path_progress(self, time):
        time = time*self.move_speed
        time_index = math.floor(time)
        interp = (time-time_index)
        return time_index, interp

    def get_position_at_simulation_end(self):
        time_index, _ = self.get_path_progress(const.sim_time)
        return sf.Vector2(*self.path[min(len(self.path)-1, time_index)])

    def tuplify(self):
        return (self.id, self.position.x, self.position.y)
