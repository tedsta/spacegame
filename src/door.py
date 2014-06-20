import sfml as sf
import src.res as res

class Door:

    """Door connects pos_a to pos_b
    """

    def __init__(self, pos_a, pos_b):
        # Horizontal
        if pos_b-pos_a == sf.Vector2(1, 0):
            self.sprite = sf.Sprite(res.door_h)
        # Vertical
        elif pos_b-pos_a == sf.Vector2(0, 1):
            self.sprite = sf.Sprite(res.door_v)
        # WTF?
        else:
            #TODO
            pass
        self.closed = True
        self.pos_a = pos_a
        self.pos_b = pos_b
