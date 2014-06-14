#!/usr/bin/env python

###################
# game state stuff

plan = 0
simulate = 1

turn_time = 10
sim_time = 5

###################
# networking stuff

packet_plans = 0
packet_next_turn = 1

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
