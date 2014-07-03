import src.res as res
from src.spritesheet import SpriteSheet

class Projectile:
    def __init__(self):
        self.sprite = sf.SpriteSheet(res.blue_crew)
        self.sprite.init(1, 1)

    def apply_simulation_time(self, time):
        pass
