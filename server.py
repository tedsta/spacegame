#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.input_system import InputSystem
from src.battle_state import ServerBattleState
from src.ship import Ship

try:
    # Create the server connection
    server = net.Server(30000)

    # Wait for connections
    print("Waiting for connections...")
    packets = server.wait_for_connections(2)
    ships = {}
    while len(ships) < 2:
        for client_id, c_packets in packets.items():
            for packet in c_packets:
                ships[client_id] = Ship()
                ships[client_id].deserialize(packet)
        packets = server.update()

    # Send players their enemy ships
    for client_id in ships:
        for enemy_id, enemy_ship in ships.items():
            if enemy_id == client_id:
                continue
            packet = net.Packet()
            packet.write(enemy_id)
            enemy_ship.serialize(packet)
            server.send(client_id, packet)
    
    # Create the battle state
    print("Starting game")
    battle_state = ServerBattleState(server, ships)
    
except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

# start the game loop
while True:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        dt_accum = 0
        frame_accum = 0

    # Update the server
    server.update()
