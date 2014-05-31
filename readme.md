# FTL Clone

## Plan
 - Update turn time (switch to simulate mode at 0)
     - On switch to simulation, send plans to server
 - Handle weapon selection and targeting
 - Handle crew commanding
 - Draw game
     - Draw background
     - Draw ships
     - Draw crew
         - Draw healthbar
     - Draw drones
     - Draw weapons
     - Draw projectiles
     - Draw beams
     - Draw GUI

## Simulate
 - Update simulation
     - Update projectiles
         - Two stages: ship to offscreen, enter target screen to hit location
     - Update beams
         - Beam orientation as interpolation from target start and end
     - Update crew
         - Crew positions are precalculated at each path step.
         - Calculate path step index based on time since simulation start
     - Update drones
         - TODO
 - Draw game
     - Draw background
     - Draw ships
     - Draw crew
         - Draw healthbar
     - Draw drones
     - Draw weapons
     - Draw projectiles
     - Draw beams
     - Draw GUI