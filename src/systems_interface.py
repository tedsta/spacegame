#!/usr/bin/env python

import sfml as sf

from src.input_system import MouseHandler
from src.rect import contains
import src.const as const

class SystemButton():
    def __init__(self, rectangle, system):
        self.rectangle = rectangle
        self.system = system


class SystemsInterface(MouseHandler):

    BUTTON_OFFSET_X = 80
    BUTTON_OFFSET_Y = 330
    BUTTON_WIDTH = 64
    BUTTON_HEIGHT = 48
    BUTTON_RIGHT_MARGIN = 10
    SYSTEM_UNPOWERED_COLOR = sf.Color(255, 255, 255)
    SYSTEM_POWERED_COLOR = sf.Color(128, 128, 128)
    BAR_POWERED_COLOR = sf.Color(128, 128, 128)

    def __init__(self, lock_window, lock_window_sprite, ship):
        self.ship = ship
        self.buttons = []  # A list of SystemButton objects
        
        self.unpowered_bar = sf.RectangleShape()
        self.unpowered_bar.fill_color = self.sf.Color(0, 0, 0, 0)
        self.unpowered_bar.outline_thickness = 2
        self.unpowered_bar.outline_color = sf.Color(255, 255, 255, 255)
        
        self.powered_bar = sf.RectangleShape()
        self.powered_bar.fill_color = self.SYSTEM_POWERED_COLOR
        #self.powered_bar.outline_thickness = 3
        #self.powered_bar.outline_color = sf.Color(0, 0, 0, 0)

        self.add_button(self.ship.engine_system)
        self.add_button(self.ship.weapon_system)

    def add_button(self, system):
        x_offset = self.BUTTON_OFFSET_X + (len(self.buttons) * (self.BUTTON_WIDTH + self.BUTTON_RIGHT_MARGIN)) + self.BUTTON_RIGHT_MARGIN
        next_button_location = sf.Vector2(x_offset, self.BUTTON_OFFSET_Y)
        rectangle = sf.RectangleShape()
        rectangle.position = next_button_location
        rectangle.size = sf.Vector2(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        rectangle.fill_color = self.SYSTEM_UNPOWERED_COLOR
        if system.power > 0:
            rectangle.fill_color = self.SYSTEM_POWERED_COLOR
        self.buttons.append(WeaponButton(rectangle, system))

    
    def on_mouse_button_pressed(self, mouse_button, x, y):
        ## LEFT CLICK ##
        if mouse_button == sf.Mouse.LEFT:
            # Left click in targeting mode exits targeting mode
            if self.targeted_weapon_button:
                self.targeted_weapon_button.rectangle.fill_color = self.SYSTEM_POWERED_COLOR
                self.targeted_weapon_button = None
                return

            # Check to see if clicked on WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    # TODO change internal color
                    if button.weapon.powered:
                        self.targeted_weapon_button = button
                        button.rectangle.fill_color = self.WEAPON_TARGETED_COLOR
                    else:
                        button.weapon.powered = True
                        button.rectangle.fill_color = self.SYSTEM_POWERED_COLOR
                        
        ## RIGHT CLICK ##
        elif mouse_button == sf.Mouse.RIGHT:
            # Check to see if clicked on a WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    if button.weapon.powered:
                        button.weapon.powered = False
                        button.rectangle.fill_color = self.SYSTEM_UNPOWERED_COLOR
                        return
            # Check to see if in targeting mode and clicked on a valid enemy room
            if self.targeted_weapon_button:
                if not self.enemy_ships:
                    return
                for ship in self.enemy_ships:
                    for room in ship.rooms:
                        room_rect = sf.Rectangle()
                        room_rect.position = ship.sprite.position+ship.room_offset+(room.position*const.block_size)
                        room_rect.size = sf.Vector2(room.width*const.block_size, room.height*const.block_size)
                        if room_rect.contains(sf.Vector2(x, y) - self.lock_window_sprite.position):
                            self.targeted_weapon_button.weapon.target = room
                            self.targeted_weapon_button.rectangle.fill_color = self.SYSTEM_POWERED_COLOR
                            self.targeted_weapon_button = None
    
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        target_selected = False
        if self.targeted_weapon_button:
            for ship in self.enemy_ships:
                for room in ship.rooms:
                    room_rect = sf.Rectangle()
                    room_rect.position = ship.sprite.position+ship.room_offset+(room.position*const.block_size)
                    room_rect.size = sf.Vector2(room.width*const.block_size, room.height*const.block_size)
                    if room_rect.contains(position - self.lock_window_sprite.position):
                        target_selected = True
                        # outline room rect
                        self.enemy_target.position = room_rect.position
                        self.enemy_target.size = room_rect.size
                        self.enemy_target.outline_color = self.TARGETED_ROOM_OUTLINE_COLOR
        if not target_selected:
            self.enemy_target.outline_color = sf.Color(0, 0, 0, 0)

    def draw(self, target):
        if self.enemy_target:
            self.lock_window.draw(self.enemy_target)
        for button in self.buttons:
            target.draw(button.rectangle)



