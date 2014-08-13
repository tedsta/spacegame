#!/usr/bin/env python

import math
import random
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.crew_interface import CrewInterface
from src.weapons_interface import WeaponsInterface
from src.systems_interface import SystemsInterface
from src.path import find_path
from src.projectile import Projectile

class ClientBattleState(net.Handler):

    def __init__(self, input, client, ships):
        self.input = input
        self.client = client

        client.add_handler(self)
        
        # Enemy render window
        self.lock_window = sf.RenderTexture(500, 500)
        self.lock_window_sprite = sf.Sprite(self.lock_window.texture)
        self.lock_window_sprite.position = (500, 50)
        
        # Ships
        self.ships = ships
        self.player_ship = self.ships[self.client.client_id]
        self.enemy_ship = None
        self.losers = []
        
        # Create the crew interface
        self.crew_interface = CrewInterface(self.player_ship)
        self.input.add_mouse_handler(self.crew_interface)
        
        # Create the systems interface
        self.systems_interface = SystemsInterface(self.player_ship)
        self.input.add_mouse_handler(self.systems_interface)

        # Create the weapons interface
        self.weapons_interface = WeaponsInterface(self.lock_window, self.lock_window_sprite, self.player_ship)
        for client_id, ship in self.ships.items():
            if client_id != self.client.client_id:
                self.weapons_interface.add_enemy_ship(ship)
                print("added enemy ship: " + str(ship))
                self.enemy_ship = ship # TODO
        self.input.add_mouse_handler(self.weapons_interface)
        self.input.add_text_handler(self.weapons_interface)
        
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

        # System index
        self.system_index = {}
        for ship in ships.values():
            ship.engine_system.id = ship.id+":engine_sys"
            ship.weapon_system.id = ship.id+":weapon_sys"
            ship.shield_system.id = ship.id+":shield_sys"
            self.system_index[ship.engine_system.id] = ship.engine_system
            self.system_index[ship.weapon_system.id] = ship.weapon_system
            self.system_index[ship.shield_system.id] = ship.shield_system
        
        # Weapon index and projectiles
        self.weapon_index = {}
        self.projectiles = []
        for ship in ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                self.weapon_index[weapon.id] = weapon
                self.projectiles.extend(weapon.projectiles)
        
        # Client ship's projectiles
        if self.player_ship.weapon_system:
            for weapon in self.player_ship.weapon_system.weapons:
                for projectile in weapon.projectiles:
                    projectile.is_mine = True

    def update(self, dt):
        if self.mode == const.plan:
            self.plan(dt)
        elif self.mode == const.simulate:
            self.simulate(dt)
        
        #self.weapons_interface.update(dt)

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
        # Send system poweredness
        # TODO
        systems_power = {}
        systems_power[self.player_ship.engine_system.id] = self.player_ship.engine_system.power
        systems_power[self.player_ship.weapon_system.id] = self.player_ship.weapon_system.power
        systems_power[self.player_ship.shield_system.id] = self.player_ship.shield_system.power
        packet.write(systems_power)
        # Send weapon poweredness (map weapon ids to bool) and targets
        weapon_powered = {} # {weap_id : room_id}
        weapon_targets = {} # {weap_id : bool}
        if self.player_ship.weapon_system:
            for weapon in self.player_ship.weapon_system.weapons:
                weapon_powered[weapon.id] = weapon.powered
                if weapon.target:
                    weapon_targets[weapon.id] = weapon.target.id
                else:
                    weapon_targets[weapon.id] = None
        packet.write(weapon_powered)
        packet.write(weapon_targets)
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
        
        # Update sprites
        for ship in self.ships.values():
            ship.update_sprites(dt)
        for projectile in self.projectiles:
            if projectile.active:
                projectile.sprite.update(dt)
            elif projectile.phase == 2: # Phase 2: detonation
                projectile.explosion_sprite.update(dt)
                if projectile.explosion_sprite.loop_done: # Explosion ended
                    projectile.phase = 0

    def apply_simulation_time(self, time):
        # Simulate crew
        for ship in self.ships.values():
            for crew in ship.crew:
                crew.apply_simulation_time(time)

        # Simulate weapons
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                weapon.apply_simulation_time(time)
                
        # Simulate projectiles
        for projectile in self.projectiles:
            if projectile.active:
                projectile.apply_simulation_time(time)

        # See if any ships died
        for ship in self.ships.values():
            if ship.alive and ship.hull_points <= 0:
                ship.blow_up()
                
    def end_simulation(self):
        for ship in self.ships.values():
            for crew in ship.crew:
                # Set crew's position to where it reaches at the end of the simulation
                crew.position = crew.get_position_at_simulation_end()
                # Update crew's current room for crew interface
                crew.current_room = ship.room_at(crew.position.x, crew.position.y)
                # Repair room if applicable
                if not crew.path and crew.current_room.system and crew.current_room.system.damage > 0:
                    crew.current_room.system.damage -= 1
                # Clear path
                crew.path[:] = []
                # Check if crew reached destination
                if crew.position == crew.destination:
                    crew.destination = None
            
            # Weapons
            if ship.weapon_system:
                for weapon in ship.weapon_system.weapons:
                    weapon.was_powered = weapon.powered
                    for projectile in weapon.projectiles:
                        projectile.active = False
                    
            # Shields
            if ship.shield_system:
                if ship.shield_system.shields < ship.shield_system.max_shields:
                    ship.shield_system.shields += 1

            # Update sprites for any visual changes (system damage color)
            ship.update_sprites(0)

        # Check for ship deaths
        for ship in self.ships.values():
            if not ship.alive:
                self.losers.append(ship)

        # Check for game over:
        if len(self.ships)-len(self.losers) < 2:
            self.mode = const.game_over
        else:
            # Increment turn
            self.mode = const.plan
            self.turn_timer = 0 # Reset turn timer
            self.turn_number += 1

    ########################################
    # Drawing
    
    def draw(self, target):
        self.lock_window.clear(sf.Color.BLACK)
    
        # Draw ships
        #for ship in self.ships.values():
        #    ship.draw(target)
        self.player_ship.draw(target)
        self.enemy_ship.draw(self.lock_window)

        # Draw projectiles
        for projectile in self.projectiles:
            if projectile.active:
                if projectile.phase == 0: # Weapon to offscreen
                    if projectile.is_mine:
                        target.draw(projectile.sprite)
                    else:
                        self.lock_window.draw(projectile.sprite)
                elif projectile.phase == 1: # Offscreen to target
                    if projectile.is_mine:
                        self.lock_window.draw(projectile.sprite)
                    else:
                        target.draw(projectile.sprite)
            elif projectile.phase == 2: # Detonation, but projectile isn't active
                if projectile.is_mine:
                    self.lock_window.draw(projectile.explosion_sprite)
                else:
                    target.draw(projectile.explosion_sprite)
        
        # Draw crew interface
        self.crew_interface.draw(target)
        
        # Draw systems interface
        self.systems_interface.draw(target)

        # Draw weapons interface
        self.weapons_interface.draw(target)

        # Draw ship hull points
        #for ship in self.ships.values():
        #    for i in range(0, ship.hull_points):
        #        res.ship_hull_point_rect.position = ship.position + sf.Vector2(2 + i*16, -50)
        #        target.draw(res.ship_hull_point_rect)
        self.player_ship.draw_hull_points(target)
        self.enemy_ship.draw_hull_points(self.lock_window)
                
        self.lock_window.display()
        target.draw(self.lock_window_sprite)
        
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
        elif self.mode == const.game_over:
            if self.player_ship in self.losers:
                if len(self.ships)-len(self.losers) > 0:
                    self.turn_mode_text.string = "You lose"
                else:
                    self.turn_mode_text.string = "Tie!"
            else:
                self.turn_mode_text.string = "You win!"
            target.draw(self.turn_mode_text)

    ########################################
    # Networking

    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_sim_result:
            self._handle_simulation_results(packet)
            self.mode = const.simulate

    def _handle_simulation_results(self, packet):
        # Crew paths
        paths_dict = packet.read()
        for crew_id, path in paths_dict.items():
            self.crew_index[crew_id].path = path
        # System stuff
        systems_power = packet.read()
        for system_id, power in systems_power.items():
            self.system_index[system_id].power = power
            self.system_index[system_id].on_power_changed()
        # Weapon stuff
        weapon_powered = packet.read() # {weap_id : room_id}
        weapon_targets = packet.read() # {weap_id : bool}
        projectile_hits = packet.read() # {weap_id : [(proj_index, bool)]}
        # Weapon targets
        for weap_id, powered in weapon_powered.items():
            self.weapon_index[weap_id].powered = powered
        # Weapon on/off
        for weap_id, target_id in weapon_targets.items():
            if target_id:
                self.weapon_index[weap_id].target = self.room_index[target_id]
            else:
                self.weapon_index[weap_id].target = None
        # Projectile hits
        for weap_id, proj_hits in projectile_hits.items():
            # Weapon is firing if there's any projectile hits
            if len(proj_hits) > 0:
                self.weapon_index[weap_id].firing = True
            else:
                self.weapon_index[weap_id].firing = False
            # Projectile hits
            for hit_tup in proj_hits:
                proj_index = hit_tup[0]
                hit = hit_tup[1]
                hit_shields = hit_tup[2]
                weapon = self.weapon_index[weap_id]
                projectile = weapon.projectiles[proj_index]
                projectile.target_room = self.weapon_index[weap_id].target
                projectile.hit = hit
                projectile.hit_shields = hit_shields
                projectile.phase = 0
                # Projectile travel path stuff
                projectile.start_position = weapon.sprite.position + sf.Vector2(30, 0)
                projectile.to_offscreen_position = weapon.sprite.position + sf.Vector2(1200, 0)
                projectile.from_offscreen_position = weapon.sprite.position + sf.Vector2(-100, -100)
                if projectile.hit_shields:
                    target = weapon.target.sprite.position+weapon.target.sprite.global_bounds.size/2
                    projectile.target_position = (target-projectile.from_offscreen_position)/2.5 + projectile.from_offscreen_position
                else:
                    projectile.target_position = weapon.target.sprite.position+weapon.target.sprite.global_bounds.size/2
                # Timing stuff
                projectile.fire_time = proj_index*0.5 # Fire each projectile half a second after the previous
                if projectile.hit_shields:
                    projectile.hit_time = projectile.fire_time+3
                else:
                    projectile.hit_time = projectile.fire_time+3 # Hit 3 seconds after fire

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

        # System index
        self.system_index = {}
        for ship in ships.values():
            ship.engine_system.id = ship.id+":engine_sys"
            ship.weapon_system.id = ship.id+":weapon_sys"
            ship.shield_system.id = ship.id+":shield_sys"
            self.system_index[ship.engine_system.id] = ship.engine_system
            self.system_index[ship.weapon_system.id] = ship.weapon_system
            self.system_index[ship.shield_system.id] = ship.shield_system
        
        # Weapon index
        self.weapon_index = {}
        for ship in ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                self.weapon_index[weapon.id] = weapon
    
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()

        if packet_id == const.packet_plans:
            # Make sure turn number matches up
            turn_number = packet.read()
            if turn_number != self.turn_number:
                return
            ship = self.ships[client_id]
            # Handle crew paths
            for crew_id, destination in packet.read().items():
                self.crew_index[crew_id].destination = sf.Vector2(*destination)
            # Systems
            systems_power = packet.read()
            for system_id, power in systems_power.items():
                self.system_index[system_id].power = power
                self.system_index[system_id].on_power_changed()
            # Receive weapon plans
            # Weapon on/off
            weapon_powered = packet.read()
            for weap_id, powered in weapon_powered.items():
                self.weapon_index[weap_id].powered = powered
            # Weapon targets
            weapon_targets = packet.read()
            for weap_id, target_id in weapon_targets.items():
                if target_id:
                    self.weapon_index[weap_id].target = self.room_index[target_id]
                else:
                    self.weapon_index[weap_id].target = None
            # Received plans
            self.received_plans[client_id] = True
            # Check if all plans have been received for this turn
            if False not in self.received_plans.values():
                # Send results
                self.prepare_simulation()
                self.send_simulation_results()
                self.end_simulation()
                # Reset for next turn
                self.received_plans = {client_id:False for client_id in self.ships.keys()}
                # Increment turn number
                self.turn_number += 1

    def prepare_simulation(self):
        self.calculate_crew_paths()

        # Do weapons
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                if weapon.powered and weapon.target:
                    weapon.firing = True
                    for projectile in weapon.projectiles:
                        if weapon.target.ship.engine_system.power == 0:
                            projectile.hit = True
                            if weapon.target.ship.shield_system and weapon.target.ship.shield_system.shields > 0:
                                projectile.hit_shields = True
                                weapon.target.ship.shield_system.shields -= projectile.damage
                            else:
                                projectile.hit_shields = False
                        else:
                            evade_chance = random.randrange(0, 100)
                            if evade_chance >= 50:
                                projectile.hit = True
                                if weapon.target.ship.shield_system and weapon.target.ship.shield_system.shields > 0:
                                    projectile.hit_shields = True
                                    weapon.target.ship.shield_system.shields -= projectile.damage
                                else:
                                    projectile.hit_shields = False
                            else:
                                projectile.hit = False
                else:
                    weapon.firing = False

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
        # Send system power
        systems_power = {}
        for id, system in self.system_index.items():
            systems_power[id] = system.power
        packet.write(systems_power)
        # Send weapon results
        weapon_powered = {} # {weap_id : room_id}
        weapon_targets = {} # {weap_id : bool}
        projectile_hits = {} # {weap_id : [(proj_index, bool)]}
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                weapon_powered[weapon.id] = weapon.powered
                if weapon.target:
                    weapon_targets[weapon.id] = weapon.target.id
                else:
                    weapon_targets[weapon.id] = None
                hits = []
                if weapon.firing:
                    for i, projectile in enumerate(weapon.projectiles):
                        hits.append((i, projectile.hit, projectile.hit_shields))
                projectile_hits[weapon.id] = hits
        packet.write(weapon_powered)
        packet.write(weapon_targets)
        packet.write(projectile_hits)
        # Send results packet
        self.server.broadcast(packet)

    def end_simulation(self):
        # Move crew
        for ship in self.ships.values():
            for crew in ship.crew:
                # Move
                crew.position = crew.get_position_at_simulation_end() 
                # Update crew's current room
                crew.current_room = ship.room_at(crew.position.x, crew.position.y)
                # Repair room if applicable
                if not crew.path and crew.current_room.system and crew.current_room.system.damage > 0:
                    crew.current_room.system.damage -= 1
                # Clear crew paths for next turn
                crew.destination = None
                crew.path[:] = []

        # Deal projectile damage
        for ship in self.ships.values():
            if not ship.weapon_system:
                continue
            for weapon in ship.weapon_system.weapons:
                if weapon.firing:
                    for projectile in weapon.projectiles:
                        if projectile.hit:
                            weapon.target.ship.hull_points -= projectile.damage
                            if weapon.target.system:
                                weapon.target.system.deal_damage(projectile.damage)
                                
        # Shields
        for ship in self.ships.values():
            if ship.shield_system:
                if ship.shield_system.shields < ship.shield_system.max_shields:
                    ship.shield_system.shields += 1
