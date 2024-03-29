#!/usr/bin/env python

import copy

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [None]*(width*height)
    
    def get(self, x, y):
        return self.data[y*self.height + x]
    
    def set(self, x, y, value):
        self.data[y*self.height + x] = value

    def fill(self, value):
        self.data = [copy.deepcopy(value) for i in range(0, self.width*self.height)]
