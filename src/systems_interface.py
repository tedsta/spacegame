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
    BUTTON_OFFSET_Y = 400
    BUTTON_WIDTH = 64
    BUTTON_HEIGHT = 48
    BUTTON_RIGHT_MARGIN = 10
    SYSTEM_UNPOWERED_COLOR = sf.Color(255, 255, 255)
    SYSTEM_POWERED_COLOR = sf.Color(128, 128, 128)
    BAR_POWERED_COLOR = sf.Color(100, 255, 100)

    def __init__(self, ship):
        self.ship = ship
        self.buttons = []  # A list of SystemButton objects
        
        self.unpowered_bar = sf.RectangleShape()
        self.unpowered_bar.fill_color = sf.Color(0, 0, 0, 0)
        self.unpowered_bar.outline_thickness = 2
        self.unpowered_bar.outline_color = sf.Color(255, 255, 255, 255)
        
        self.powered_bar = sf.RectangleShape()
        self.powered_bar.size = sf.Vector2(32, 8)
        self.powered_bar.fill_color = self.BAR_POWERED_COLOR
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
        self.buttons.append(SystemButton(rectangle, system))

    
    def on_mouse_button_pressed(self, mouse_button, x, y):
        ## LEFT CLICK ##
        if mouse_button == sf.Mouse.LEFT:
            # Check to see if clicked on SystemButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    # TODO change internal color
                    if button.system.get_max_usable_power() > button.system.power:
                        button.system.power += 1
                        
        ## RIGHT CLICK ##
        elif mouse_button == sf.Mouse.RIGHT:
            # Check to see if clicked on a SystemButton
            for button in self.buttons:
                if contains(button.rectangle, sf.Vector2(x, y)):
                    if button.system.power > 0:
                        button.system.power -= 1
                        return
    
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass

    def draw(self, target):
        for button in self.buttons:
            if button.system.power > 0:
                button.rectangle.fill_color = self.SYSTEM_POWERED_COLOR
            else:
                button.rectangle.fill_color = self.SYSTEM_UNPOWERED_COLOR
            target.draw(button.rectangle)
            for i in range(0, button.system.max_power):
                if i < button.system.power:
                    self.powered_bar.position = button.rectangle.position+sf.Vector2(3, button.rectangle.size.y-((self.powered_bar.size.y+2)*(i+1))-3)
                    target.draw(self.powered_bar)
                elif i < button.system.max_power:
                    self.unpowered_bar.position = button.rectangle.position+sf.Vector2(3, button.rectangle.size.y-((self.powered_bar.size.y+2)*(i+1))-3)
                    target.draw(self.unpowered_bar)



