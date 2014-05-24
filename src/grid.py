#!/usr/bin/env python

class Grid:

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._data = [None]*(width*height)
    
    @property
    def width(self): return self._width
    @property
    def height(self): return self._height
    
    def get(self, x, y):
        return self._data[y*self._height + x]
    
    def set(self, x, y, value):
        self._data[y*self._height + x] = value