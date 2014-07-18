from src.system import System

class EngineSystem(System):
    def __init__(self):
        System.__init__(self)
        self.max_power = 1
        self.power = 1
