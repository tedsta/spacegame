#!/usr/bin/env python

import math
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.crew_interface import CrewInterface

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
        packet = net.Packet()
        packet.write(const.packet_plans)
        # Write turn number
        packet.write(self.turn_number)
        # Build crew destinations dictionary
        crew_destinations = {}
        for crew in self.player_ship.crew:
            if crew.destination:
                crew_destinations[crew.id] = (crew.destination.x, crew.destination.y)
        packet.write(crew_destinations)
        # Send the plans
        self.client.send(packet)

        # Switch to wait mode
        self.turn_timer = 0 # Reset turn timer
        self.mode = const.wait
    
    ########################################
    # Simulate

    def simulate(self, dt):
        # Update turn timer
        self.turn_timer += dt
        if self.turn_timer >= const.sim_time:
            self.end_simulation()
            return

        # Apply simulation
        self.apply_simulation_time(self.turn_timer)

    def apply_simulation_time(self, time):
        for ship in self.ships.values():
            for crew in ship.crew:
                if not crew.path: # Skip crew with no path
                    continue
                time_index = math.floor(time)
                interp_time = time-time_index
                if time_index+1 >= len(crew.path): # Reached end of path
                    position = sf.Vector2(*crew.path[-1])
                else:
                    start_pos = sf.Vector2(*crew.path[time_index])
                    end_pos = sf.Vector2(*crew.path[time_index+1])
                    position = start_pos + (end_pos-start_pos)*interp_time
                crew.position = position
                crew.sprite.position = ship.sprite.position+ship.room_offset+(position*const.block_size)

    def end_simulation(self):
        for ship in self.ships.values():
            for crew in ship.crew:
                if not crew.path:
                    continue
                crew.position = sf.Vector2(*crew.path[-1])
                crew.sprite.position = ship.sprite.position+ship.room_offset+(crew.position*const.block_size)
                # Clear path
                crew.path[:] = []
                # Check if crew reached destination
                if crew.position == crew.destination:
                    crew.destination = None

        # Increment turn
        self.mode = const.plan
        self.turn_timer = 0 # Reset turn timer
        self.turn_number += 1
    
    def draw(self, target):
        # Draw ships
        for ship in self.ships.values():
            ship.draw(target)
        
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
            paths_dict = packet.read()
            for crew_id, path in paths_dict.items():
                self.crew_index[crew_id].path = path
            self.mode = const.simulate


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
    
    def update(self, dt):
        # Check if all plans have been received for this turn
        if False not in self.received_plans.values():
            # Send results
            self.calculate_crew_paths()
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
            # Received plans
            self.received_plans[client_id] = True

    def calculate_crew_paths(self):
        for crew in self.crew_index.values():
            if not crew.destination:
                crew.path[:] = []
                continue
            crew.path = [(crew.position.x, crew.position.y), (crew.destination.x, crew.destination.y)]
            # Apply path
            crew.position = sf.Vector2(*crew.path[-1])
            # Check if crew reached his destination
            if crew.position == crew.destination:
                crew.destination = None

    def send_simulation_results(self):
        packet = net.Packet()
        packet.write(const.packet_sim_result)
        paths_dict = {}
        for crew in self.crew_index.values():
            paths_dict[crew.id] = crew.path
        packet.write(paths_dict)
        self.server.broadcast(packet)
