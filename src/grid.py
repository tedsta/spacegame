#!/usr/bin/env python

from collections import namedtuple

WalkDirs = namedtuple("walkdirs", "up_left up up_right left right down_left down down_right")

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [None]*(width*height)
    
    def get(self, x, y):
        return self.data[y*self.height + x]
    
    def set(self, x, y, value):
        self.data[y*self.height + x] = value

