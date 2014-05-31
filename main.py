#!/usr/bin/env python

import sfml as sf

from src.input_system import InputSystem
import src.res as res
from src.ship import Ship

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "pySFML Window")
window.key_repeat_enabled = False

input = InputSystem(window)

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Create a ship
    ship = Ship()
    ship.add_room(res.room2x2, 0, 0)
    ship.add_room(res.room2x2, 0, 2)
    ship.add_room(res.room2x1, 1, 2)
    
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

    # Handle input
    input.handle()
    
    ## Draw
    
    window.clear(sf.Color(120, 120, 120)) # clear screen
    
    ship.draw(window)
    
    # Draw framerate
    window.draw(frame_rate)
    
    window.display() # update the window