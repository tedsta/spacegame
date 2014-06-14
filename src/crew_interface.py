#!/usr/bin/env python

import sfml as sf

import src.const as const
from src.input_system import MouseHandler
from src.rect import intersects

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
            for crew in self.selected_crew:
                crew.set_highlighted(False)
            self.selected_crew[:] = []
            self._selecting = True
            self._select_start = sf.Vector2(x, y)
            # Reset draw rectangle
            self._rectangle.position = self._select_start
            self._rectangle.size = sf.Vector2(0, 0)
        elif button == sf.Mouse.RIGHT:
            # Right mouse button pressed - set destination
            # First, find selected room
            target_room = None
            for room in self._ship._rooms:
                room_rect = sf.Rectangle()
                room_rect.position = self._ship._sprite.position+self._ship._room_offset+(room.position*const.block_size)
                room_rect.size = sf.Vector2(room.width*const.block_size, room.height*const.block_size)
                if room_rect.contains(sf.Vector2(x, y)):
                    target_room = room
            if not target_room:
                return # No room targeted
            for crew in self.selected_crew:
                if target_room.is_full():
                    break
                crew.destination = target_room.get_free_position()
    
    def on_mouse_button_released(self, button, x, y):
        if button == sf.Mouse.LEFT and self._selecting:
            # Left mouse button released during selection - finish drag selection
            self._selecting = False
            
            # Find all crew in selection area
            select_rect = sf.Rectangle(self._rectangle.position, self._rectangle.size)
            for crew in self._ship._crew:
                crew_left, crew_top, crew_width, crew_height = crew.sprite.global_bounds
                crew_rect = sf.Rectangle(sf.Vector2(crew_left, crew_top), sf.Vector2(crew_width, crew_height))
                if intersects(select_rect, crew_rect):
                    crew.set_highlighted(True)
                    self.selected_crew.append(crew)
                else:
                    crew.set_highlighted(False)
    
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
            
            # Find all crew in selection area
            select_rect = sf.Rectangle(self._rectangle.position, self._rectangle.size)
            for crew in self._ship._crew:
                crew_left, crew_top, crew_width, crew_height = crew.sprite.global_bounds
                crew_rect = sf.Rectangle(sf.Vector2(crew_left, crew_top), sf.Vector2(crew_width, crew_height))
                if intersects(select_rect, crew_rect):
                    crew.set_highlighted(True)
                else:
                    crew.set_highlighted(False)
    
    def draw(self, target):
        if self._selecting:
            target.draw(self._rectangle)
