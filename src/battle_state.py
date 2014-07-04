#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.crew_interface import CrewInterface
from src.path import find_path
from src.projectile import Projectile

class ClientBattleState(net.Handler):

    def __init__(self, input, client, ships):
        self.input = input
        self.client = client

        client.add_handler(self)
        
        # Ships
        self.ships = ships
        self.player_ship = self.ships[self.client.client_id]
        
        # Create the crew interface
        self.crew_interface = CrewInterface(self.player_ship)
        self.input.add_mouse_handler(self.crew_interface)
        
        # Turn stuff
        self.mode = const.plan
        self.turn_timer = 0
        self.turn_number = 0
        
        # Timer text
        self.turn_mode_text = sf.Text("0", res.font_8bit, 20)
        self.turn_mode_text.position = sf.Vector2(400, 30)

        # Crew index
        self.crew_index = {}
        for ship in ships.values():
            for crew in ship.crew:
                self.crew_index[crew.id] = crew
        
        # Room index
        self.room_index = {}
        for ship in ships.values():
            for room in ship.rooms:
                self.room_index[room.id] = room
        
        # Weapon index
        self.weapon_index = {}
        for ship in ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                self.weapon_index[weapon.id] = weapon

        # Projectiles
        self.projectiles = []
    
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
            self.end_turn()
            return
    
        # Handle input
        self.input.handle()

    def end_turn(self):
        # Send plans packet
        self._send_plans_packet()

        # Switch to wait mode
        self.turn_timer = 0 # Reset turn timer
        self.mode = const.wait

    def _send_plans_packet(self):
        packet = net.Packet()
        packet.write(const.packet_plans)
        # Write turn number
        packet.write(self.turn_number)
        # Write crew destinations dictionary
        crew_destinations = self._build_crew_destinations_dictionary()
        packet.write(crew_destinations)
        # Send to server
        self.client.send(packet)

    def _build_crew_destinations_dictionary(self):
        crew_destinations = {}
        for crew in self.player_ship.crew:
            if crew.destination:
                crew_destinations[crew.id] = (crew.destination.x, crew.destination.y)
        return crew_destinations
    
    ########################################
    # Simulate

    def simulate(self, dt):
        # Handle window events
        for event in self.input.window.events:
            # close window: exit
            if type(event) is sf.CloseEvent:
                self.window.close()
    
        # Update turn timer
        self.turn_timer += dt
        if self.turn_timer >= const.sim_time:
            self.end_simulation()
            return

        # Apply simulation
        self.apply_simulation_time(self.turn_timer)

    def apply_simulation_time(self, time):
        # Simulate crew
        for ship in self.ships.values():
            for crew in ship.crew:
                crew.apply_simulation_time(time)

        # Simulate projectiles
        for projectile in self.projectiles:
            if projectile.active:
                projectile.apply_simulation_time(time)
                
    def end_simulation(self):
        for ship in self.ships.values():
            for crew in ship.crew:
                # Set crew's position to where it reaches at the end of the simulation
                crew.position = crew.get_position_at_simulation_end()
                # Update crew's current room for crew interface
                crew.current_room = ship.room_at(crew.position.x, crew.position.y)
                # Clear path
                crew.path[:] = []
                # Check if crew reached destination
                if crew.position == crew.destination:
                    crew.destination = None

        # Increment turn
        self.mode = const.plan
        self.turn_timer = 0 # Reset turn timer
        self.turn_number += 1

    ########################################
    # Drawing
    
    def draw(self, target):
        # Draw ships
        for ship in self.ships.values():
            ship.draw(target)

        # Draw projectiles
        for projectile in self.projectiles:
            if projectile.active:
                target.draw(projectile.sprite)
        
        # Draw crew interface
        self.crew_interface.draw(target)
        
        # Draw timer
        if self.mode == const.plan:
            self.turn_mode_text.string = str(math.floor(const.turn_time-self.turn_timer))
            target.draw(self.turn_mode_text)
        elif self.mode == const.wait:
            self.turn_mode_text.string = "Waiting..."
            target.draw(self.turn_mode_text)
        elif self.mode == const.simulate:
            self.turn_mode_text.string = "Simulating"
            target.draw(self.turn_mode_text)

    ########################################
    # Networking

    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_sim_result:
            self._handle_simulation_results(packet)

    def _handle_simulation_results(self, packet):
        # Crew paths
        paths_dict = packet.read()
        for crew_id, path in paths_dict.items():
            self.crew_index[crew_id].path = path
        self.mode = const.simulate
        # Weapon stuff
        weapon_targets = packet.read()
        weapon_activations = packet.read()
        projectile_hits = packet.read()

###############################################################################
# Server

class ServerBattleState(net.Handler):

    def __init__(self, server, ships):
        self.server = server
        self.server.add_handler(self)

        # Setup ships
        self.ships = ships
        self.received_plans = {client_id:False for client_id in self.ships.keys()}

        # Turn stuff
        self.turn_number = 0
        
        # Crew index
        self.crew_index = {}
        for ship in ships.values():
            for crew in ship.crew:
                self.crew_index[crew.id] = crew

        # Room index
        self.room_index = {}
        for ship in ships.values():
            for room in ship.rooms:
                self.room_index[room.id] = room
        
        # Weapon index
        self.weapon_index = {}
        for ship in ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                self.weapon_index[weapon.id] = weapon
    
    def update(self, dt):
        # Check if all plans have been received for this turn
        if False not in self.received_plans.values():
            # Send results
            self.apply_simulation()
            self.send_simulation_results()
            # Reset for next turn
            self.received_plans = {client_id:False for client_id in self.ships.keys()}
            # Increment turn number
            self.turn_number += 1

    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_plans:
            # Make sure turn number matches up
            turn_number = packet.read()
            if turn_number != self.turn_number:
                return
            # Handle crew paths
            for crew_id, destination in packet.read().items():
                self.crew_index[crew_id].destination = sf.Vector2(*destination)
            # TODO Receive weapon plans
            # Received plans
            self.received_plans[client_id] = True

    def apply_simulation(self):
        self.calculate_crew_paths()

        # Do weapons
        # TODO
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                if not weapon.target:
                    continue
                for projectile in weapon.projectiles:
                    projectile.hit = True

        # Move crew
        for ship in self.ships.values():
            for crew in ship.crew:
                crew.position = crew.get_position_at_simulation_end() 

    def calculate_crew_paths(self):
        for ship in self.ships.values():
            for crew in ship.crew:
                if not crew.destination:
                    continue
                pos = (crew.position.x, crew.position.y)
                dest = (crew.destination.x, crew.destination.y)
                crew.path = find_path(ship.path_grid, pos, dest) # coming soon!

    def send_simulation_results(self):
        packet = net.Packet()
        packet.write(const.packet_sim_result)
        # Crew paths
        paths_dict = {}
        for crew in self.crew_index.values():
            paths_dict[crew.id] = crew.path
        packet.write(paths_dict)
        # Clear crew paths for next turn
        for crew in self.crew_index.values():
            crew.destination = None
            crew.path[:] = []
        # Send weapon results
        weapon_targets = {} # {weap_id : room_id}
        weapon_activations = {} # {weap_id : bool}
        projectile_hits = {} # {weap_id : [(proj_index, bool)]}
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                if not weapon.target:
                    continue
                weapon_targets[weapon.id] = weapon.target.id
                weapon_activations[weapon.id] = weapon.active
                for i, projectile in enumerate(weapon.projectiles):
                    projectile_hits[weapon.id] = (i, projectile.hit)
        packet.write(weapon_targets)
        packet.write(weapon_activations)
        packet.write(projectile_hits)
        # Send results packet
        self.server.broadcast(packet)
