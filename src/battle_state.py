#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
from src.crew_interface import CrewInterface

class ClientBattleState:

    PLAN = 0
    SIMULATE = 1
    TURN_TIME = 10

    def __init__(self, input, player_ship, enemy_ship=None):
        self._input = input
        
        # Set player and enemy ships
        self._player_ship = player_ship
        self._enemy_ship = enemy_ship
        
        # Create the crew interface
        self._crew_interface = CrewInterface(self._player_ship)
        self._input.add_mouse_handler(self._crew_interface)
        
        # Turn stuff
        self._mode = ClientBattleState.PLAN
        self._turn_timer = 0
        
        # Timer text
        self._timer_text = sf.Text("0", res.font_8bit, 20)
        self._timer_text.position = sf.Vector2(400, 30)
    
    def update(self, dt):
        if self._mode == ClientBattleState.PLAN:
            self._plan(dt)
        elif self._mode == ClientBattleState.SIMULATE:
            self._simulate(dt)
    
    def _plan(self, dt):
        # Update turn timer
        self._turn_timer += dt
        if self._turn_timer >= ClientBattleState.TURN_TIME:
            self._mode = ClientBattleState.SIMULATE
            self._turn_timer = 0 # Reset turn timer
    
        # Handle input
        self._input.handle()
    
    def _simulate(self, dt):
        self._mode = ClientBattleState.PLAN
    
    def draw(self, target):
        self._player_ship.draw(target)
        
        # Draw timer
        if self._mode == ClientBattleState.PLAN:
            self._timer_text.string = str(math.floor(ClientBattleState.TURN_TIME-self._turn_timer))
            target.draw(self._timer_text)