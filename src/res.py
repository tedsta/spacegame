#!/usr/bin/env python

import sfml as sf

###################
# crew stuff

crew = sf.Texture.from_file("content/textures/crew/operative_sprite.png")
blue_crew = sf.Texture.from_file("content/textures/crew/blue.png")
blue_crew_highlighted = sf.Texture.from_file("content/textures/crew/blue_highlighted.png")

human_base = sf.Texture.from_file("content/textures/crew/human_base.png")
human_color = sf.Texture.from_file("content/textures/crew/human_color.png")

###################
# ship stuff

ship = sf.Texture.from_file("content/textures/ships/ship.png")

ship_piece1 = sf.Texture.from_file("content/textures/ships/ship_piece1.png")
ship_piece2 = sf.Texture.from_file("content/textures/ships/ship_piece2.png")
ship_piece3 = sf.Texture.from_file("content/textures/ships/ship_piece3.png")
ship_piece4 = sf.Texture.from_file("content/textures/ships/ship_piece4.png")
ship_piece5 = sf.Texture.from_file("content/textures/ships/ship_piece5.png")
ship_piece6 = sf.Texture.from_file("content/textures/ships/ship_piece6.png")

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
sf.Texture.from_file("content/textures/rooms/1x2.png"),\
sf.Texture.from_file("content/textures/rooms/2x2.png"),\
sf.Texture.from_file("content/textures/rooms/2x2.png"),\
]

# room overlays
room_overlays = [\
None,\
None,\
None,\
sf.Texture.from_file("content/textures/rooms/room_pilot1x2.png"),\
sf.Texture.from_file("content/textures/rooms/room_engines2x2.png"),\
sf.Texture.from_file("content/textures/rooms/room_weapons2x2.png"),\
]

# room icons
room_icons = [\
None,\
None,\
None,\
sf.Texture.from_file("content/textures/rooms/icon_pilot.png"),\
sf.Texture.from_file("content/textures/rooms/icon_engines.png"),\
sf.Texture.from_file("content/textures/rooms/icon_weapons.png"),\
]

###################
# door stuff

door_h = sf.Texture.from_file("content/textures/rooms/door_h.png")
door_v = sf.Texture.from_file("content/textures/rooms/door_v.png")

###################
# weapons

weapon = sf.Texture.from_file("content/textures/weapons/laser.png")

###################
# Projectiles

laser_light1 = sf.Texture.from_file("content/textures/weapons/laser_light1.png")

###################
# Effects

explosion_missile1 = sf.Texture.from_file("content/textures/effects/explosion_missile1.png")

###################
# GUI
button = sf.Texture.from_file("content/textures/gui/button.png")
textbox = sf.Texture.from_file("content/textures/gui/textbox.png")

###################
# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")
