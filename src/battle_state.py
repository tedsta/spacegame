#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.crew_interface import CrewInterface

class ClientBattleState(net.Handler):

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
        packet.write(const.packet_plans)
        # Build crew destinations dictionary
        crew_destinations = {}
        for crew in self.player_ship._crew:
            crew_destinations[crew.id] = (crew.destination.x, crew.destination.y)
        packet.write(crew_destinations)
        # Send the plans
        self.client.send(packet)
    
    ########################################
    # Simulate

    def simulate(self, dt):
        # Update turn timer
        self.turn_timer += dt
        if self.turn_timer >= const.sim_time:
            self.mode = const.plan
            self.turn_timer = 0 # Reset turn timer
            self.end_simulation()

    def apply_simulation_time(self, time):
        for crew in self.player_ship._crew:
            crew.sprite.position = sf.Vector2(0, 0) # TODO

    def end_simulation(self):
        for crew in self.player_ship._crew:
            crew.position = crew.destination
            crew.sprite.position = self.player_ship._sprite.position+self.player_ship._room_offset+(crew.position*const.block_size)
    
    def draw(self, target):
        self.player_ship.draw(target)
        
        # Draw crew interface
        self.crew_interface.draw(target)
        
        # Draw timer
        if self.mode == const.plan:
            self.timer_text.string = str(math.floor(const.turn_time-self.turn_timer))
            target.draw(self.timer_text)
        elif self.mode == const.simulate:
            self.timer_text.string = "Simulating"
            target.draw(self.timer_text)

    ########################################
    # Networking

    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_next_turn:
            pass


###############################################################################
# Server

class ServerBattleState(net.Handler):

    def __init__(self, server, player_ship, enemy_ship=None):
        self.server = server
        self.server.add_handler(self)

        # Set player and enemy ships
        self.player_ship = player_ship
        self.enemy_ship = enemy_ship
        
        # Turn stuff
        self.mode = const.plan
        self.turn_timer = 0
        
        # Timer text
        self.timer_text = sf.Text("0", res.font_8bit, 20)
        self.timer_text.position = sf.Vector2(400, 30)

        # Crew index
        self.crew_index = {}
    
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
    
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_plans:
            for crew_id, destination in packet.read().items():
                self.crew_index[crew_id].destination = destination
