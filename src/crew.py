#!/usr/bin/env python

import sfml as sf

import src.res as res
from src.spritesheet import SpriteSheet

class Crew:

    def __init__(self):
        self.id = 0
        self.position = sf.Vector2(0, 0) # Position on ship grid
        self.sprite = SpriteSheet(res.blue_crew)
        self.sprite.init(1, 1)
        self.path = []
        self.highlighted = False
        self.destination = None # Plan destination
    
    def set_highlighted(self, highlight):
        if highlight:
            self.sprite.texture = res.blue_crew_highlighted
        else:
            self.sprite.texture = res.blue_crew
        self.highlighted = highlight

    def tuplify(self):
        return ()
