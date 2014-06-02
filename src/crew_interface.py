#!/usr/bin/env python

import sfml as sf

from src.input_system import MouseHandler

class CrewInterface(MouseHandler):

    def __init__(self, ship):
        # Selected crew members
        self.selected_crew = []
        
        # Player ship to select crew from
        self._ship = ship
    
        # Internal selection stuff
        self._selecting = False
        self._select_start = sf.Vector2(0, 0)
        self._select_stop = sf.Vector2(0, 0)
    
    def on_mouse_button_pressed(self, button, x, y):
        if button == sf.Mouse.LEFT:
            # Left mouse button pressed - begin drag select
            self._selecting = True
            self._select_start = sf.Vector2(x, y)
    
    def on_mouse_button_released(self, button, x, y):
        if button == sf.Mouse.LEFT and self._selecting:
            # Left mouse button released during selection - finish drag selection
            
            # First, make select_start represent top left, and select_stop represent bottom right
            self._select_stop = sf.Vector2(max(x, self._select_start.x), max(y, self._select_start.y))
            self._select_start = sf.Vector2(min(x, self._select_start.x), min(y, self._select_start.y))
            
            # Find all crew in selection area
    
    def on_mouse_moved(self, position, move):
        pass