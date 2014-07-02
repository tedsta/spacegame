from src.system import System

class WeaponSystem(System):
    def __init__(self):
        System.__init__(self)
        self.weapons = []
