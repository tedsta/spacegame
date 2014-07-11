#!/usr/bin/env python

import sfml as sf

from src.input_system import MouseHandler
from src.rect import contains
import src.const as const

class WeaponButton():
    def __init__(self, rectangle, weapon):
        self.rectangle = rectangle
        self.weapon = weapon

    def __str__(self):
        return "WeaponButton for weapon " + str(self.weapon) +\
                " at rectangle " + str(self.rectangle)


class WeaponsInterface(MouseHandler):

    BUTTON_OFFSET_X = 80
    BUTTON_OFFSET_Y = 330
    BUTTON_WIDTH = 30
    BUTTON_HEIGHT = 30
    BUTTON_RIGHT_MARGIN = 10
    WEAPON_UNPOWERED_COLOR = sf.Color(255, 255, 255)
    WEAPON_POWERED_COLOR = sf.Color(128, 128, 128)
    WEAPON_TARGETED_COLOR = sf.Color(0, 255, 0)
    TARGETED_ROOM_OUTLINE_COLOR = sf.Color(255, 255, 0)

    def __init__(self, ship):
        self.ship = ship
        self.enemy_ships = []
        self.current_weapon = None
        self.buttons = []  # A list of WeaponButton objects
        self.targeted_weapon_button = None
        self.enemy_target = sf.RectangleShape()
        self.enemy_target.fill_color = sf.Color(0, 0, 0, 0) # transparent
        self.enemy_target.outline_thickness = 3
        self.enemy_target.outline_color = sf.Color(0, 0, 0, 0)

        for weapon in self.ship.weapon_system.weapons:
            self.add_button(weapon)

    def add_enemy_ship(self, ship):
        self.enemy_ships.append(ship)

    def add_button(self, weapon):
        x_offset = self.BUTTON_OFFSET_X + (len(self.buttons) * (self.BUTTON_WIDTH + self.BUTTON_RIGHT_MARGIN)) + self.BUTTON_RIGHT_MARGIN
        next_button_location = sf.Vector2(x_offset, self.BUTTON_OFFSET_Y)
        rectangle = sf.RectangleShape()
        rectangle.position = next_button_location
        rectangle.size = sf.Vector2(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        rectangle.fill_color = self.WEAPON_UNPOWERED_COLOR
        if weapon.powered:
            rectangle.fill_color = self.WEAPON_POWERED_COLOR
        self.buttons.append(WeaponButton(rectangle, weapon))

    
    def on_mouse_button_pressed(self, mouse_button, x, y):
        ## LEFT CLICK ##
        if mouse_button == sf.Mouse.LEFT:
            # Left click in targeting mode exits targeting mode
            if self.targeted_weapon_button:
                self.targeted_weapon_button.rectangle.fill_color = self.WEAPON_POWERED_COLOR
                self.targeted_weapon_button = None
                print("weapon untargeted")
                return

            # Check to see if clicked on WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    # TODO change internal color
                    if button.weapon.powered:
                        self.targeted_weapon_button = button
                        button.rectangle.fill_color = self.WEAPON_TARGETED_COLOR
                        print("weapon targeted")
                    else:
                        button.weapon.powered = True
                        button.rectangle.fill_color = self.WEAPON_POWERED_COLOR
                        
        ## RIGHT CLICK ##
        elif mouse_button == sf.Mouse.RIGHT:
            # Check to see if clicked on a WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    if button.weapon.powered:
                        button.weapon.powered = False
                        button.rectangle.fill_color = self.WEAPON_UNPOWERED_COLOR
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
                        if room_rect.contains(sf.Vector2(x, y)):
                            self.targeted_weapon_button.weapon.target = room
                            print("weapon targeted on " + str(room))
                            self.targeted_weapon_button.rectangle.fill_color = self.WEAPON_POWERED_COLOR
                            self.targeted_weapon_button = None
                            print("weapon untargeted")
    
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
                    if room_rect.contains(position):
                        target_selected = True
                        # outline room rect
                        self.enemy_target.position = room_rect.position
                        self.enemy_target.size = room_rect.size
                        self.enemy_target.outline_color = self.TARGETED_ROOM_OUTLINE_COLOR
        if not target_selected:
            self.enemy_target.outline_color = sf.Color(0, 0, 0, 0)

    def draw(self, target):
        if self.enemy_target:
            target.draw(self.enemy_target)
        for button in self.buttons:
            target.draw(button.rectangle)



