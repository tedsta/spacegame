import src.res as res

class Weapon:
    def __init__(self, id):
        self.id = id
        self.active = False
        self.target = None
        self.charge = 0
        self.required_charge = 1
        self.power = 1 # Power consumption
        self.projectile_type = None
        self.num_shots = 1
        self.sprite = res.weapon
