"""
Combat moves to be used within combat module. Moves are objects generated by player/AI action during combat.
"""
from termcolor import colored, cprint
import random
import states, functions

class Move: #master class for all moves
    def __init__(self, name, description, xp_gain, current_stage, beats_left,
                 stage_announce, target, user, stage_beat, targeted, heat_gain=0, fatigue_cost=0):
        self.name = name
        self.description = description
        self.xp_gain = xp_gain
        self.heat_gain = heat_gain
        self.current_stage = current_stage
        self.stage_beat = stage_beat
        self.beats_left = beats_left
        self.stage_announce = stage_announce
        self.fatigue_cost = fatigue_cost
        self.target = target  # can be the same as the user in abilities with no targets
        self.user = user
        self.targeted = targeted  # Is the move targeted at something?
        self.interrupted = False  # When a move is interrupted, skip all remaining actions for that move, set the
        # move's cooldown
        self.initialized = False

    def process_stage(self, user):
        if user.current_move == self:
            if self.current_stage == 0:
                self.prep(user)
            elif self.current_stage == 1:
                self.execute(user)
            elif self.current_stage == 2:
                self.recoil(user)
            elif self.current_stage == 3:
                self.cooldown(user)  # the cooldown stage will typically never be rewritten,
                # so this will usually just pass

    def cast(self, user): # this is what happens when the ability is first chosen by the player
        self.current_stage = 0 # initialize prep stage
        if self.stage_announce[0] != "":
            print(self.stage_announce[0])  # Print the prep announce message for the move
        self.beats_left = self.stage_beat[0]

    def advance(self, user):
        if user.current_move == self or self.current_stage == 3: # only advance the move if it's the player's
            # current move or if it's in cooldown
            if self.beats_left > 0:
                self.beats_left -= 1
            else:
                while self.beats_left == 0: # this loop will advance stages until the current stage has a beat count,
                    # effectively skipping unused stages
                    self.process_stage(user)
                    self.current_stage += 1  # switch to next stage
                    if self.current_stage == 3: # when the move enters cooldown, detach it from the player so he can
                        # do something else.
                        user.current_move = None
                        self.initialized = False
                    if self.current_stage > 3: # if the move is coming out of cooldown, switch back to the prep stage
                        # and break the while loop
                        self.current_stage = 0
                        self.beats_left = self.stage_beat[self.current_stage]
                        break
                    self.beats_left = self.stage_beat[self.current_stage]  # set beats remaining for current stage

    def prep(self, user): #what happens during these stages. Each move will overwrite prep/execute/recoil/cooldown
        # depending on whether something is supposed to happen at that stage
        # print("######{}: I'm in the prep stage now".format(self.name)) #debug message
        pass

    def execute(self, user):
        # print("######{}: I'm in the execute stage now".format(self.name)) #debug message
        if self.stage_announce[1] != "":
            print(self.stage_announce[1])

    def recoil(self, user):
        # print("######{}: I'm in the recoil stage now".format(self.name)) #debug message
       if self.stage_announce[2] != "":
            print(self.stage_announce[2])

    def cooldown(self, user):
        # print("######{}: I'm in the cooldown stage now".format(self.name)) #debug message
        pass

    def check_parry(self, target):
        parry = False
        for state in target.states:
            if state.name == "Parrying":
                parry = True
                break
        return parry



### ANY MOVES ###

class Dodge(Move):
    def __init__(self, user):
        description = "Prepare to dodge incoming attacks."
        prep = 1
        execute = 1
        recoil = 5
        cooldown = 2
        fatigue_cost = 75 - ((2 * user.endurance) + (3 * user.speed))
        if fatigue_cost <= 10:
            fatigue_cost = 10
        super().__init__(name="Dodge", description=description, xp_gain=1, current_stage=0,
                         stage_beat=[prep,execute,recoil,cooldown], targeted=False,
                         stage_announce=["",
                                         "{} tenses in preparation to avoid attacks.".format(user.name),
                                         "",
                                         ""], fatigue_cost=fatigue_cost, beats_left=prep,
                         target=user, user=user)

    def execute(self, user):
        # print("######{}: I'm in the execute stage now".format(self.name)) #debug message
        print(self.stage_announce[1])
        self.user.states.append(states.Dodging(user))
        self.user.fatigue -= self.fatigue_cost

class Parry(Move):
    def __init__(self, user):
        description = "Attempt to parry the next incoming attack."
        prep = 1
        execute = 1
        recoil = 5
        cooldown = 2
        fatigue_cost = 75 - ((2 * user.endurance) + (3 * user.speed))
        if fatigue_cost <= 10:
            fatigue_cost = 10
        super().__init__(name="Parry", description=description, xp_gain=1, current_stage=0,
                         stage_beat=[prep, execute, recoil, cooldown], targeted=False,
                         stage_announce=["",
                                         "{} attempts to parry the next attack.".format(user.name),
                                         "",
                                         ""], fatigue_cost=fatigue_cost, beats_left=prep,
                         target=user, user=user)

    def execute(self, user):
        # print("######{}: I'm in the execute stage now".format(self.name)) #debug message
        print(self.stage_announce[1])
        self.user.states.append(states.Parrying(user))
        self.user.fatigue -= self.fatigue_cost

### PLAYER MOVES ###

class Wait(Move):  # player chooses how many beats he'd like to wait
    def __init__(self, player):
        description = "Wait for the right opportunity to make your move."
        prep = 0
        execute = 0
        recoil = 0
        cooldown = 0
        fatigue_cost = 0
        super().__init__(name="Wait", description=description, xp_gain=0, current_stage=0,
                         targeted=False,
                         stage_beat=[prep,execute,recoil,cooldown],
                         stage_announce=["Jean is waiting.",
                                         "",
                                         "",
                                         ""], fatigue_cost=fatigue_cost,
                         beats_left=execute, target=player, user=player)

    def execute(self, player):
        duration = ''
        while functions.is_input_integer(duration) == False:
            duration = input("Number of beats to wait (min 3, max 10): ", )
            if functions.is_input_integer(duration):
                duration = int(duration)
                if duration > 10 or duration < 3:
                    cprint("You must enter a duration between 3 and 10 beats.", "red")
                    duration = ''
        self.stage_beat[2] = duration - 2



class Attack(Move): #basic attack function, always uses equipped weapon, player only
    def __init__(self, player):
        description = "Strike at your enemy with your equipped weapon."
        power = player.eq_weapon.damage + \
                    (player.strength * player.eq_weapon.str_mod) + \
                    (player.finesse * player.eq_weapon.fin_mod)
        prep = int(50 / player.speed) #starting prep of 5
        if prep < 1:
            prep = 1
        execute = 1
        recoil = int(1 + player.eq_weapon.weight)
        cooldown = 5 - int(player.speed/10)
        if cooldown < 0:
            cooldown = 0
        weapon = player.eq_weapon.name
        fatigue_cost = 100 - (5 * player.endurance)
        if fatigue_cost <= 10:
            fatigue_cost = 10
        super().__init__(name="Attack", description=description, xp_gain=1, current_stage=0,
                         stage_beat=[prep,execute,recoil,cooldown], targeted=True,
                         stage_announce=["Jean winds up for a strike...",
                                         colored("Jean strikes with his " + weapon + "!", "green"),
                                         "Jean braces himself as his weapon recoils.",
                                         ""], fatigue_cost=fatigue_cost, beats_left=prep,
                         target=None, user=player)
        self.power = power

    def execute(self, player):
        # print("######{}: I'm in the execute stage now".format(self.name)) #debug message
        print(self.stage_announce[1])
        hit_chance = (95 - self.target.finesse) + self.user.finesse
        if hit_chance <= 0:
            hit_chance = 1
        roll = random.randint(0, 100)
        damage = ((self.power - self.target.protection) * player.heat) * random.uniform(0.8, 1.2)
        damage = int(damage)
        player.combat_exp += 500  # todo change this back to 10 when testing is done
        if hit_chance >= roll: #a hit!
            if self.check_parry(self.target):
                print(colored(self.target.name, "magenta") + colored(" parried the attack!", "red"))
                self.stage_beat[2] += 10
                player.change_heat(0.75)
            else:
                print(colored(self.target.name, "magenta") + colored(" was struck for ", "yellow") +
                      colored(damage, "red") + colored(" damage!", "yellow"))
                self.target.hp -= damage
                # print("######{}'s HP is {}".format(self.target.name, self.target.hp)) #debug msg
                player.change_heat(1.25)
        else:
            print(colored("Just missed!", "white"))
            player.change_heat(0.75)
        self.user.fatigue -= self.fatigue_cost

class Rest(Move):  # standard rest to restore fatigue.
    def __init__(self, player):
        description = "Rest for a moment to restore fatigue."
        prep = 1
        execute = 1
        recoil = 2
        cooldown = 0
        fatigue_cost = 0
        super().__init__(name="Rest", description=description, xp_gain=0, current_stage=0,
                         targeted=False,
                         stage_beat=[prep,execute,recoil,cooldown],
                         stage_announce=["Jean relaxes his muscles for a moment.",
                                         colored("Jean is resting.", "green"),
                                         "",
                                         ""], fatigue_cost=fatigue_cost,
                         beats_left=execute, target=player, user=player)

    def execute(self, player):
        print(self.stage_announce[1])
        recovery_amt = (player.maxfatigue * 0.4) * random.uniform(0.8, 1.2)
        recovery_amt = int(recovery_amt)
        if recovery_amt > player.maxfatigue - player.fatigue:
            recovery_amt = player.maxfatigue - player.fatigue
        player.fatigue += recovery_amt
        cprint("You recovered {} FP!".format(recovery_amt), "green")
        player.combat_exp += 2

class Use_Item(Move): #basic attack function, always uses equipped weapon
    def __init__(self, player):
        description = "Use an item from your inventory."
        prep = 1
        execute = 1
        recoil = 1
        cooldown = 0
        fatigue_cost = 0
        super().__init__(name="Use Item", description=description, xp_gain=0, current_stage=0,
                         targeted=False,
                         stage_beat=[prep,execute,recoil,cooldown],
                         stage_announce=["Jean opens his bag.",
                                         "",
                                         "Jean closes his bag.",
                                         ""], fatigue_cost=fatigue_cost,
                         beats_left=execute, target=player, user=player)

    def execute(self, player):
        player.use_item() # opens the category view for the standard "use item" action
        player.combat_exp += 1

### NPC MOVES ###

class NPC_Attack(Move): #basic attack function, NPCs only
    def __init__(self, npc):
        description = ""
        power = (npc.damage * random.uniform(0.8, 1.2))

        prep = int(50 / npc.speed)
        if prep < 1:
            prep = 1

        execute = 1

        recoil = int(50 / npc.speed)
        if recoil < 0:
            recoil = 0

        cooldown = 5 - int(npc.speed/10)
        if cooldown < 0:
            cooldown = 0

        fatigue_cost = 100 - (5 * npc.endurance)
        if fatigue_cost <= 10:
            fatigue_cost = 10

        if npc.target == None:
            npc.target = npc

        super().__init__(name="NPC_Attack", description=description, xp_gain=1, current_stage=0,
                         stage_beat=[prep,execute,recoil,cooldown], targeted=True,
                         stage_announce=[colored("{} coils in preparation for an attack!".format(npc.name), "red"),
                                         colored("{} lashes out at {} with "
                                                 "extreme violence!".format(npc.name, npc.target.name), "red"),
                                         "{} recoils from the attack.".format(npc.name),
                                         ""],
                         fatigue_cost=fatigue_cost, beats_left=prep,
                         target=npc.target, user=npc)
        self.power = power

    def refresh_announcements(self, npc):
        self.stage_announce = [colored("{} coils in preparation for an attack!".format(npc.name), "red"),
                          colored("{} lashes out at {} with "
                                  "extreme violence!".format(npc.name, self.target.name), "red"),
                          "{} recoils from the attack.".format(npc.name),
                          ""]

    def execute(self, npc):
        self.refresh_announcements(npc)
        print(self.stage_announce[1])
        hit_chance = (95 - self.target.finesse) + self.user.finesse
        if hit_chance <= 0:
            hit_chance = 1
        roll = random.randint(0, 100)
        damage = (self.power - self.target.protection)
        damage = int(damage)
        if hit_chance >= roll: #a hit!
            if self.check_parry(self.target):
                print(colored(self.target.name, "magenta") + colored(" parried the attack!", "yellow"))
                self.stage_beat[2] += 10
                if self.target.name == "Jean":
                    self.target.change_heat(1.4)
            print(colored(self.user.name, "magenta") + colored(" hit {} for ".format(self.target.name), "yellow") +
                  colored(damage, "red") + colored(" damage!", "yellow"))
            self.target.hp -= damage
            self.target.change_heat(1 - (damage / self.target.maxhp))  # reduce heat by the percentage of dmg done to
            #  maxhp
        else:
            print(colored("{}'s attack just missed!".format(self.user.name), "white"))
            if self.user.target.name == "Jean":
                for state in self.user.target.states:
                    if state.name == "Dodging":
                        self.user.target.change_heat(1.25)
                        break
                self.user.target.change_heat(1.1)
        self.user.fatigue -= self.fatigue_cost

class NPC_Rest(Move):  # standard rest to restore fatigue for NPCs.
    def __init__(self, npc):
        description = "Rest for a moment to restore fatigue."
        prep = 0
        execute = 1
        recoil = 2
        cooldown = 0
        fatigue_cost = 0
        super().__init__(name="Rest", description=description, xp_gain=0, current_stage=0,
                         targeted=False,
                         stage_beat=[prep,execute,recoil,cooldown],
                         stage_announce=["{} rests for a moment.".format(npc.name),
                                         colored("{} is resting.".format(npc.name), "white"),
                                         "",
                                         ""], fatigue_cost=fatigue_cost,
                         beats_left=execute, target=npc, user=npc)

    def execute(self, npc):
        print(self.stage_announce[1])
        recovery_amt = (self.user.maxfatigue * 0.25) * random.uniform(0.8, 1.2)
        recovery_amt = int(recovery_amt)
        if recovery_amt > self.user.maxfatigue - self.user.fatigue:
            recovery_amt = self.user.maxfatigue - self.user.fatigue
        self.user.fatigue += recovery_amt


class NPC_Idle(Move):  # NPC does nothing for a few beats.
    def __init__(self, npc):
        description = "What?"
        prep = 0
        execute = 3
        recoil = 0
        cooldown = 0
        fatigue_cost = 0
        super().__init__(name="Idle", description=description, xp_gain=0, current_stage=0,
                         targeted=False,
                         stage_beat=[prep,execute,recoil,cooldown],
                         stage_announce=["",
                                         str(npc.name + npc.idle_message),
                                         "",
                                         ""], fatigue_cost=fatigue_cost,
                         beats_left=execute, target=npc, user=npc)

    def execute(self, npc):
        print(self.stage_announce[1])