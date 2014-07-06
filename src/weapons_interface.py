#!/usr/bin/env python

import sfml as sf

import src.const as const
from src.input_system import MouseHandler
from src.rect import intersects


class WeaponsInterface(MouseHandler):

    def __init__(self, ship):
        """
        # Selected crew members
        self.selected_crew = []
        
        # Player ship to select crew from
        self.ship = ship
    
        # Internal selection stuff
        self.selecting = False
        self.select_start = sf.Vector2(0, 0)
        self.select_stop = sf.Vector2(0, 0)
        
        # Draw stuff
        In addition, make buttons semi-pretty. For example, highlight the buttons whose weapons are in active. Double highlight button if the weapon is in targetting mode. (gray, white, and green are the colors in FTL)
        self.rectangle = sf.RectangleShape()
        self.rectangle.outline_color = sf.Color(0, 255, 0)
        self.rectangle.fill_color = sf.Color(0, 255, 0, 100)
        self.rectangle.outline_thickness = 2
        """
        pass
    
    def on_mouse_button_pressed(self, button, x, y):
        """
        If you left click a deactivated weapon button, the weapon becomes active.
        If you left click an activated weapon button, you enter targetting mode for that weapon.
        If you left click in targetting mode, you exit targetting mode.
        If you right click in targetting mode, check if an enemy room was clicked. If so, target the selected weapon to the clicked room. (i.e. selected_weapon.target = room)

        if button == sf.Mouse.LEFT:
            # Left mouse button pressed - begin drag select
            for crew in self.selected_crew:
                crew.set_highlighted(False)
            self.selected_crew[:] = []
            self.selecting = True
            self.select_start = sf.Vector2(x, y)
            # Reset draw rectangle
            self.rectangle.position = self.select_start
            self.rectangle.size = sf.Vector2(0, 0)
        elif button == sf.Mouse.RIGHT:
            # Right mouse button pressed - set destination
            # First, find selected room
            target_room = None
            for room in self.ship.rooms:
                room_rect = sf.Rectangle()
                room_rect.position = self.ship.sprite.position+self.ship.room_offset+(room.position*const.block_size)
                room_rect.size = sf.Vector2(room.width*const.block_size, room.height*const.block_size)
                if room_rect.contains(sf.Vector2(x, y)):
                    target_room = room
            if not target_room:
                return # No room targeted
            # Set each selected crew's destination to the target room
            for crew in self.selected_crew:
                # No more space in target room - break out
                if target_room.is_full():
                    break
                if crew.destination:
                    # Crew has prior destination - freeup the old destination
                    crew.target_room.freeup_position(crew.destination)
                else:
                    # Crew has no prior destination - freeup it's current position
                    crew.current_room.freeup_position(crew.position)
                # Set new destination stuff
                crew.destination = target_room.get_free_position()
                crew.target_room = target_room
                """
        pass
    
    def on_mouse_button_released(self, button, x, y):
        """
        if button == sf.Mouse.LEFT and self.selecting:
            # Left mouse button released during selection - finish drag selection
            self.selecting = False

            self._update_selections(sf.Vector2(x, y))
            """
        pass
            
    def on_mouse_moved(self, position, move):
        """
        if self.selecting:
            self._update_selections(position) 
            """
        pass

    def draw(self, target):
        """
        if self.selecting:
            target.draw(self.rectangle)
            """
        pass

    #############################################

    def _update_selections(self, position):
        """Updates selected crew.
        position: Mouse position in pixels
        """
        """
        # Set select stop
        self.select_stop = sf.Vector2(position.x, position.y)
        
        # Calculate rectangle
        left = min(position.x, self.select_start.x)
        top = min(position.y, self.select_start.y)
        right = max(position.x, self.select_start.x)
        bottom = max(position.y, self.select_start.y)
        
        # Updating drawing rectangle
        self.rectangle.position = sf.Vector2(left, top)
        self.rectangle.size = sf.Vector2(right-left, bottom-top)

        # Clear the selected crew
        self.selected_crew[:] = []
        
        # Find all crew in selection area
        select_rect = sf.Rectangle(self.rectangle.position, self.rectangle.size)
        for crew in self.ship.crew:
            crew_left, crew_top, crew_width, crew_height = crew.sprite.global_bounds
            crew_rect = sf.Rectangle(sf.Vector2(crew_left, crew_top), sf.Vector2(crew_width, crew_height))
            if intersects(select_rect, crew_rect):
                crew.set_highlighted(True)
                self.selected_crew.append(crew)
            else:
                crew.set_highlighted(False)
                """
        pass
