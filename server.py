#!/usr/bin/env python

import sfml as sf

import src.res as res
import src.const as const
import src.net as net
from src.input_system import InputSystem
from src.battle_state import ServerBattleState
from src.ship import Ship
from src.crew import Crew

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Create a ship
    ship = Ship()
    ship.add_room(const.room2x2, 0, 0)
    ship.add_room(const.room2x2, 0, 2)
    ship.add_room(const.room2x1, 1, 2)
    
    # Create a crew
    crew = Crew()
    ship.add_crew(crew, sf.Vector2(1, 1))

    # Create the server connection
    server = net.Server(30000)
    
    # Create the battle state
    battle_state = ServerBattleState(server, ship)
    
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
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update the server
    server.update()
    
    # Update game state
    battle_state.update(dt)
