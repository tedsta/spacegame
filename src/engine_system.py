from src.system import System

class EngineSystem(System):
    def __init__(self):
        System.__init__(self)
        self.max_power = 2
        self.power = 2
