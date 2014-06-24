#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.input_system import InputSystem
from src.battle_state import ClientBattleState
from src.ship import Ship
from src.crew import Crew

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Space Game")
window.key_repeat_enabled = False

input = InputSystem(window)

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Create a ship
    ship = Ship()
    ship.add_room(const.room2x2, 0, 0)
    ship.add_room(const.room2x2, 0, 2)
    ship.add_room(const.room2x2, 0, 4)
    ship.add_room(const.room2x1, 2, 3)
    ship.add_room(const.room2x1, 4, 3)
    ship.add_room(const.room2x1, 2, 5)
    ship.add_room(const.room2x2, 3, 1)
    ship.add_room(const.room2x2, 4, 4)

    # Create a crew
    ship.add_crew(Crew(), sf.Vector2(0, 0))
    ship.add_crew(Crew(), sf.Vector2(1, 0))
    ship.add_crew(Crew(), sf.Vector2(0, 1))
    ship.add_crew(Crew(), sf.Vector2(1, 1))
    ship.add_crew(Crew(), sf.Vector2(3, 1))
    
    # Connect to server
    client = net.Client("localhost", 30000)

    # Setup crew IDs
    for i, crew in enumerate(ship.crew):
        crew.id = client.client_id+":crew"+str(i)

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
            other_ship.set_position(sf.Vector2(50, 50))
        else:
            other_ship.set_position(sf.Vector2(450, 0))
    
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
