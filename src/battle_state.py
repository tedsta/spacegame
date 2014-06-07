#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
import src.const as const
from src.crew_interface import CrewInterface

class ClientBattleState:

    def __init__(self, input, player_ship, enemy_ship=None):
        self._input = input
        
        # Set player and enemy ships
        self._player_ship = player_ship
        self._enemy_ship = enemy_ship
        
        # Create the crew interface
        self._crew_interface = CrewInterface(self._player_ship)
        self._input.add_mouse_handler(self._crew_interface)
        
        # Turn stuff
        self._mode = const.plan
        self._turn_timer = 0
        
        # Timer text
        self._timer_text = sf.Text("0", res.font_8bit, 20)
        self._timer_text.position = sf.Vector2(400, 30)
    
    def update(self, dt):
        if self._mode == const.plan:
            self._plan(dt)
        elif self._mode == const.simulate:
            self._simulate(dt)
    
    def _plan(self, dt):
        # Update turn timer
        self._turn_timer += dt
        if self._turn_timer >= const.turn_time:
            self._mode = const.simulate
            self._turn_timer = 0 # Reset turn timer
    
        # Handle input
        self._input.handle()
    
    def _simulate(self, dt):
        self._mode = const.plan
    
    def draw(self, target):
        self._player_ship.draw(target)
        
        # Draw crew interface
        self._crew_interface.draw(target)
        
        # Draw timer
        if self._mode == const.plan:
            self._timer_text.string = str(math.floor(const.turn_time-self._turn_timer))
            target.draw(self._timer_text)