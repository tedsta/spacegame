#!/usr/bin/env python

import sfml as sf

###################
# crew stuff

crew = sf.Texture.from_file("content/textures/crew/operative_sprite.png")

###################
# ship stuff

ship = sf.Texture.from_file("content/textures/ships/ship.png")

###################
# room stuff

# room textures
room_textures = [\
sf.Texture.from_file("content/textures/rooms/2x2.png"),\
sf.Texture.from_file("content/textures/rooms/2x1.png"),\
sf.Texture.from_file("content/textures/rooms/1x2.png"),\
]

###################
# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")