#!/usr/bin/env python

###################
# game state stuff

plan = 0
wait = 1
simulate = 2

turn_time = 10
sim_time = 5

sim_event_create_projectile = 0
sim_event_move_projectile = 1
sim_event_projectile_hit_room = 2

###################
# networking stuff

packet_plans = 0
packet_sim_result = 1
packet_next_turn = 2

###################
# room stuff

# room block size
block_size = 35

# room index ids
room2x2 = 0
room2x1 = 1
room1x2 = 2

# room dimensions
room_dims = [\
(2,2),\
(2,1),\
(1,2),\
]
