#!/usr/bin/env python

import sys
import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.input_system import InputSystem
from src.battle_state import ClientBattleState
from src.ship import Ship
from src.crew import Crew
from src.weapon import Weapon
from src.weapon_system import WeaponSystem

# Parse args
ip_address = "localhost"
if len(sys.argv) > 1:
    ip_address = sys.argv[1]

# create the main window
window = sf.RenderWindow(sf.VideoMode(1024, 768), "Space Game")
window.key_repeat_enabled = False

input = InputSystem(window)

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Connect to server
    client = net.Client(ip_address, 30000)

    # Create a ship
    ship = Ship(client.client_id)
    
    ship.weapon_system = WeaponSystem()

    ship.add_weapon_slot(360, 80, True, True, "right")
    ship.add_weapon_slot(360, 120, True, False, "right")
    ship.add_weapon_slot(230, 29, True, True, "up")
    ship.add_weapon_slot(300, 294, True, False, "down")

    ship.add_room(const.room2x2, 0, 0)
    ship.add_room(const.room_engines2x2, 0, 2)
    ship.add_room(const.room2x2, 0, 4)
    ship.add_room(const.room2x1, 2, 3)
    ship.add_room(const.room2x1, 4, 3)
    ship.add_room(const.room2x1, 2, 5)
    ship.add_room(const.room_weapons2x2, 3, 1)
    ship.add_room(const.room2x2, 4, 4)

    # Create a crew
    ship.add_crew(Crew(), 0, 0)
    ship.add_crew(Crew(), 1, 0)
    ship.add_crew(Crew(), 0, 1)
    ship.add_crew(Crew(), 1, 1)
    ship.add_crew(Crew(), 3, 1)

    # Weapons!!!
    ship.add_weapon(Weapon(""))
    ship.add_weapon(Weapon(""))
    ship.add_weapon(Weapon(""))

    # Setup crew IDs
    for i, crew in enumerate(ship.crew):
        crew.id = client.client_id+":crew"+str(i)

    # Setup weapon IDs
    if ship.weapon_system:
        for i, weapon in enumerate(ship.weapon_system.weapons):
            weapon.id = client.client_id+":weap"+str(i)

    # Send the server my badass ship
    ship_packet = net.Packet()
    ship.serialize(ship_packet)
    client.send(ship_packet)

    # Receive enemy ship
    ships = {client.client_id:ship}
    while len(ships) < 2:
        packets = client.update()
        for packet in packets:
            client_id = packet.read()
            enemy_ship = Ship()
            enemy_ship.deserialize(packet)
            ships.update({client_id:enemy_ship})

    for client_id, other_ship in ships.items():
        if client_id == client.client_id:
            other_ship.set_position(sf.Vector2(50, 100))
        else:
            other_ship.set_position(sf.Vector2(100, 150))
    
    # Create the battle state
    battle_state = ClientBattleState(input, client, ships)
    
except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

# start the game loop
while window.is_open:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update connection
    client.update()
    
    # Update game state
    battle_state.update(dt)
    
    ####################
    ## Draw
    
    window.clear(sf.Color(120, 120, 120)) # clear screen
    
    battle_state.draw(window)
    
    # Draw framerate
    window.draw(frame_rate)
    
    window.display() # update the window
