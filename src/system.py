class System:
    def __init__(self):
        self.id = ""
        self.power = 0
        self.max_power = 0
        self.damage = 0

    def deal_damage(self, amount):
        self.damage = min(self.damage+amount, self.max_power)
        self.power = min(self.power, self.max_power - self.damage)

    def get_max_usable_power(self):
        """Max power minus damage and ion damage
        """
        return self.max_power-self.damage
