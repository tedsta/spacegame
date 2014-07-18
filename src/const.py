#!/usr/bin/env python

###################
# game state stuff

plan = 0
wait = 1
simulate = 2
game_over = 3

turn_time = 10
sim_time = 5

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
engine_room2x2 = 0
room2x2 = 1
room2x1 = 2
room1x2 = 3

# room dimensions
room_dims = [\
(2,2),\
(2,2),\
(2,1),\
(1,2),\
]
