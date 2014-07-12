import sfml as sf
import src.res as res
from src.spritesheet import SpriteSheet

class Door:

    """Door connects pos_a to pos_b
    """

    def __init__(self, pos_a, pos_b):
        # Horizontal
        if pos_b-pos_a == sf.Vector2(1, 0):
            self.sprite = SpriteSheet(res.door_h)
            self.sprite.init(1, 1)
        # Vertical
        elif pos_b-pos_a == sf.Vector2(0, 1):
            self.sprite = SpriteSheet(res.door_v)
            self.sprite.init(1, 1)
        # WTF?
        else:
            #TODO
            pass
        self.closed = True
        self.pos_a = pos_a
        self.pos_b = pos_b
