#!/usr/bin/env python

import sfml as sf

###################
# crew stuff

crew = sf.Texture.from_file("content/textures/crew/operative_sprite.png")
blue_crew = sf.Texture.from_file("content/textures/crew/blue.png")
blue_crew_highlighted = sf.Texture.from_file("content/textures/crew/blue_highlighted.png")

###################
# ship stuff

ship = sf.Texture.from_file("content/textures/ships/ship.png")

ship_hull_point_rect = sf.RectangleShape()
ship_hull_point_rect.size = (12, 24)
ship_hull_point_rect.fill_color = sf.Color.GREEN

###################
# room stuff

# room textures
room_textures = [\
sf.Texture.from_file("content/textures/rooms/2x2.png"),\
sf.Texture.from_file("content/textures/rooms/2x1.png"),\
sf.Texture.from_file("content/textures/rooms/1x2.png"),\
]

###################
# door stuff

door_h = sf.Texture.from_file("content/textures/rooms/door_h.png")
door_v = sf.Texture.from_file("content/textures/rooms/door_v.png")

###################
# weapons

weapon = sf.Texture.from_file("content/textures/weapons/bomber.png")

###################
# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")
