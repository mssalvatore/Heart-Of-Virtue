"""
Combat moves to be used within combat module. Moves are objects generated by player/AI action during combat.
"""
from termcolor import colored
import random

class Move: #master class for all moves
    def __init__(self, name, description, xp_gain, heat_gain, current_stage, stages, stage_beat, beats_left,
                 stage_announce, fatigue_cost, cooldown_left, target, user):
        self.name = name
        self.description = description
        self.xp_gain = xp_gain
        self.heat_gain = heat_gain
        self.current_stage = current_stage
        self.stages = stages
        self.stage_beat = stage_beat
        self.beats_left = beats_left
        self.stage_announce = stage_announce
        self.fatigue_cost = fatigue_cost
        self.cooldown_left = cooldown_left
        self.target = target
        self.user = user

    def evaluate(self):
        if not self.current_stage == "cooldown":
            state = [self.current_stage, self.beats_left] #todo: Here's where I left off last

class PlayerAttack(Move): #basic attack function, always uses equipped weapon
    def __init__(self, player):
        description = "Strike at your enemy with your equipped weapon."
        power = player.eq_weapon.damage + \
                (player.strength * player.eq_weapon.str_mod) + \
                (player.finesse * player.eq_weapon.fin_mod)
        prep = 1
        execute = 1
        recoil = 1 + player.eq_weapon.weight
        cooldown = 5 - (player.speed/10)
        if cooldown < 0:
            cooldown = 0
        weapon = player.eq_weapon.name
        fatigue_cost = 100 - (7 * player.endurance)
        if fatigue_cost <= 10:
            fatigue_cost = 10
        super().__init__(name="Attack", description=description, xp_gain=1, heat_gain= 0.1, current_stage=0,
                         stages= ["prep", "execute", "recoil"], stage_beat=[prep,execute,recoil],
                         stage_announce=["You wind up for a strike...",
                                         colored("You strike with your " + weapon + "!", "green"),
                                         "You brace yourself as your weapon recoils.",
                                         "You are ready to attack again."], fatigue_cost=fatigue_cost, beats_left=prep,
                         cooldown_left=0, target=None, user=player)
        self.power = power

    def execute(self, player, target):
        hit_chance = 95 - target.finesse + player.finesse
        roll = random.randint(0, 100)
        damage = self.power - target.armor
        if hit_chance >= roll: #a hit!
            print(colored(target.name, "magenta") + colored(" was struck for ", "yellow") +
                  colored(damage, "red") + colored(" damage!", "yellow"))
            target.hp -= damage
        self.current_stage = "recoil"
        self.beats_left = self.stage_beat[2]



class Rest(Move): #basic attack function, always uses equipped weapon
    def __init__(self, player):
        description = "Rest for a moment to restore fatigue."
        prep = 0
        execute = 3
        recoil = 0
        cooldown = 0
        fatigue_cost = -1 * (40 + player.endurance)
        super().__init__(name="Rest", description=description, xp_gain=0, heat_gain= 0.1, current_stage=0,
                         stages= ["prep", "execute", "recoil"], stage_beat=[prep,execute,recoil],
                         stage_announce=["You relax your muscles for a moment.",
                                         colored("You are resting.", "green"),
                                         "You brace yourself as your weapon recoils.",
                                         "You are ready to attack again."], fatigue_cost=fatigue_cost,
                         beats_left=execute, cooldown_left=0)