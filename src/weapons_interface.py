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

    def __init__(self, ship):
        self.ship = ship
        self.enemy_ships = []
        self.current_weapon = None
        self.buttons = []  # A list of WeaponButton objects
        self.targeted_weapon = None

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
        rectangle.outline_thickness = 0
        rectangle.outline_color = sf.Color(0, 255, )
        if weapon.powered:
            rectangle.outline_thickness = 5
        self.buttons.append(WeaponButton(rectangle, weapon))

    
    def on_mouse_button_pressed(self, mouse_button, x, y):
        ## LEFT CLICK ##
        if mouse_button == sf.Mouse.LEFT:
            # Left click in targetting mode exits targetting mode
            if self.targeted_weapon:
                self.targeted_weapon = None
                print("weapon untargetted")
                return

            # Check to see if clicked on WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    # TODO change internal color
                    if button.weapon.powered:
                        self.targeted_weapon = button.weapon
                        print("weapon targetted")
                        # TODO change color; maybe should store targeted_weapon_button ?
                    else:
                        button.weapon.powered = True
                        button.rectangle.outline_thickness = 5
                        
        ## RIGHT CLICK ##
        elif mouse_button == sf.Mouse.RIGHT:
            # Check to see if clicked on a WeaponButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    if button.weapon.powered:
                        button.weapon.powered = False
                        button.rectangle.outline_thickness = 0
                        return
            # Check to see if in targetting mode and clicked on a valid enemy room
            if self.targeted_weapon:
                if not self.enemy_ships:
                    return
                for ship in self.enemy_ships:
                    for room in ship.rooms:
                        room_rect = sf.Rectangle()
                        room_rect.position = ship.sprite.position+ship.room_offset+(room.position*const.block_size)
                        room_rect.size = sf.Vector2(room.width*const.block_size, room.height*const.block_size)
                        if room_rect.contains(sf.Vector2(x, y)):
                            self.targeted_weapon.target = room
                            print("weapon targeted on " + str(room))
    
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass

    def draw(self, target):
        for button in self.buttons:
            target.draw(button.rectangle)



