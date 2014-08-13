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
room2x2 = 0
room2x1 = 1
room1x2 = 2
room_pilot1x2 = 3
room_engines2x2 = 4
room_weapons2x2 = 5
room_shields2x2 = 6

# room dimensions
room_dims = [\
(2,2),\
(2,1),\
(1,2),\
(1,2),\
(2,2),\
(2,2),\
(2,2),\
]
