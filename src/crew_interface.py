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
        
        # Draw stuff
        self._rectangle = sf.RectangleShape()
        self._rectangle.outline_color = sf.Color(0, 255, 0)
        self._rectangle.fill_color = sf.Color(0, 255, 0, 100)
        self._rectangle.outline_thickness = 2
    
    def on_mouse_button_pressed(self, button, x, y):
        if button == sf.Mouse.LEFT:
            # Left mouse button pressed - begin drag select
            self._selecting = True
            self._select_start = sf.Vector2(x, y)
            # Reset draw rectangle
            self._rectangle.position = self._select_start
            self._rectangle.size = sf.Vector2(0, 0)
    
    def on_mouse_button_released(self, button, x, y):
        if button == sf.Mouse.LEFT and self._selecting:
            # Left mouse button released during selection - finish drag selection
            self._selecting = False
            
            # Find all crew in selection area
    
    def on_mouse_moved(self, position, move):
        if self._selecting:
            # Set select stop
            self._select_stop = sf.Vector2(position.x, position.y)
            
            # Calculate rectangle
            left = min(position.x, self._select_start.x)
            top = min(position.y, self._select_start.y)
            right = max(position.x, self._select_start.x)
            bottom = max(position.y, self._select_start.y)
            
            # Updating drawing rectangle
            self._rectangle.position = sf.Vector2(left, top)
            self._rectangle.size = sf.Vector2(right-left, bottom-top)
    
    def draw(self, target):
        if self._selecting:
            target.draw(self._rectangle)