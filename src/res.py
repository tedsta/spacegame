#!/usr/bin/env python

import sfml as sf

###################
# ship stuff

ship = sf.Texture.from_file("content/textures/ships/ship.png")

###################
# room stuff

# room block size
block_size = 35

# room index ids
room2x2 = 0

# room dimensions
room_dims = [\
(2,2)
]

# room textures
room_textures = [\
sf.Texture.from_file("content/textures/rooms/2x2.png"),\
]

###################
# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")