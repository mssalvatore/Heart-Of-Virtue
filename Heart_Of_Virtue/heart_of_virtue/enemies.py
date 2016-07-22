import random
import genericng

class Enemy:
    def __init__(self, name, description, damage, aggro, exp_award,
                 inventory = None, maxhp = 100, protection = 0, speed = 10, finesse = 10,
                 awareness = 10, maxfatigue = 100, endurance = 10, strength = 10, charisma = 10, intelligence = 10,
                 faith = 10,
                 idle_message = ' is shuffling about.', alert_message = 'glares sharply at you!', target = None):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.idle_message = idle_message
        self.alert_message = alert_message
        self.maxhp = maxhp
        self.hp = maxhp
        self.damage = damage
        self.protection = protection
        self.speed = speed
        self.finesse = finesse
        self.resistance = [0,0,0,0,0,0]  # this will need a separate definition when enemies are initialized
        self.awareness = awareness  # used when a player enters the room to see if npc spots the player
        self.aggro = aggro
        self.exp_award = exp_award
        self.maxfatigue = maxfatigue
        self.endurance = endurance
        self.strength = strength
        self.charisma = charisma
        self.intelligence = intelligence
        self.faith = faith
        self.fatigue = self.maxfatigue
        self.target = target
        #todo: set up targeting for NPCs during combat

    def is_alive(self):
        return self.hp > 0


class Slime(Enemy):  # target practice
    def __init__(self):
        description = "Goop that moves. Gross."
        super().__init__(name="Slime " + genericng.generate(4,5), description=description, maxhp=30,
                         damage=1, awareness=12, aggro=True, exp_award=1,
                         idle_message=" is glopping about.",
                         alert_message=" burbles angrily at you!")

class RockRumbler(Enemy):
    def __init__(self):
        description = "A burly creature covered in a rock-like carapace somewhat resembling a stout crocodile." \
                           "Highly resistant to most weapons. You'd probably be better off avoiding combat with this" \
                           "one."
        super().__init__(name="Rock Rumbler " + genericng.generate(2,4), description=description, maxhp=30,
                         damage=3, protection=30, awareness=12, aggro=True, exp_award=100)
        self.resistance = [0,0,0,0.5,0,0]  # resists earth by 50%

