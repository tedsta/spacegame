class System:
    def __init__(self):
        self.id = ""
        self.power = 0
        self.max_power = 0
        self.damage = 0

    def deal_damage(self, amount):
        old_power = self.power

        self.damage = min(self.damage+amount, self.max_power)
        self.power = min(self.power, self.max_power - self.damage)

        if old_power != self.power:
            self.on_power_changed()

    def get_max_usable_power(self):
        """Max power minus damage and ion damage
        """
        return self.max_power-self.damage

    #################################################
    # Callbacks

    def on_power_changed(self):
        pass
