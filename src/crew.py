#!/usr/bin/env python

import sfml as sf

import src.res as res

class Crew:

    def __init__(self):
        self.ship_position = sf.Vector2(0, 0) # Position on ship grid
        self.sprite = SpriteSheet(res.crew, 72, 12)
        self.path = []