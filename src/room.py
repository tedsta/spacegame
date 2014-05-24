#!/usr/bin/env python

import sfml as sf
import src.res as res

class Room:

    def __init__(self, room_type, x, y, width, height, texture):
        self.room_type = room_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sf.Sprite(texture)