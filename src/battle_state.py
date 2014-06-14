#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.crew_interface import CrewInterface

class ClientBattleState:

    def __init__(self, input, client, player_ship, enemy_ship=None):
        self.input = input
        self.client = client
        
        # Set player and enemy ships
        self.player_ship = player_ship
        self.enemy_ship = enemy_ship
        
        # Create the crew interface
        self.crew_interface = CrewInterface(self.player_ship)
        self.input.add_mouse_handler(self.crew_interface)
        
        # Turn stuff
        self.mode = const.plan
        self.turn_timer = 0
        
        # Timer text
        self.timer_text = sf.Text("0", res.font_8bit, 20)
        self.timer_text.position = sf.Vector2(400, 30)
    
    def update(self, dt):
        if self.mode == const.plan:
            self.plan(dt)
        elif self.mode == const.simulate:
            self.simulate(dt)

    ########################################
    # Plan
    
    def plan(self, dt):
        # Update turn timer
        self.turn_timer += dt
        if self.turn_timer >= const.turn_time:
            self.mode = const.simulate
            self.turn_timer = 0 # Reset turn timer
            self.end_turn()
    
        # Handle input
        self.input.handle()

    def end_turn(self):
        packet = net.Packet()
        for crew in self.player_ship._crew:
            packet.write(crew.destination.x)
            packet.write(crew.destination.y)
        self.client.send(packet)
    
    ########################################
    # Simulate

    def simulate(self, dt):
        self.mode = const.plan
    
    def draw(self, target):
        self.player_ship.draw(target)
        
        # Draw crew interface
        self.crew_interface.draw(target)
        
        # Draw timer
        if self.mode == const.plan:
            self.timer_text.string = str(math.floor(const.turn_time-self.turn_timer))
            target.draw(self.timer_text)


###############################################################################
# Server

class ServerHandler(net.Handler):

    def __init__(self):
        pass

    def handle_packet(self, packet, client_id):
        print(packet.read(), packet.read())

class ServerBattleState:

    def __init__(self, server, player_ship, enemy_ship=None):
        self.server = server

        self.net_handler = ServerHandler()
        self.server.add_handler(self.net_handler)

        # Set player and enemy ships
        self.player_ship = player_ship
        self.enemy_ship = enemy_ship
        
        # Turn stuff
        self.mode = const.plan
        self.turn_timer = 0
        
        # Timer text
        self.timer_text = sf.Text("0", res.font_8bit, 20)
        self.timer_text.position = sf.Vector2(400, 30)
    
    def update(self, dt):
        if self.mode == const.plan:
            self.plan(dt)
        elif self.mode == const.simulate:
            self.simulate(dt)
    
    def plan(self, dt):
        # Update turn timer
        self.turn_timer += dt
        if self.turn_timer >= const.turn_time:
            self.mode = const.simulate
            self.turn_timer = 0 # Reset turn timer
    
    def simulate(self, dt):
        self.mode = const.plan
    
    def draw(self, target):
        self.player_ship.draw(target)
        
        # Draw timer
        if self.mode == const.plan:
            self.timer_text.string = str(math.floor(const.turn_time-self.turn_timer))
            target.draw(self.timer_text)
