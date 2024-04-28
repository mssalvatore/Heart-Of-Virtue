"""
General events
"""
# from termcolor import colored, cprint
# import threading
# import random
# import time
from src.objects import *
from src.functions import *
from src.items import *
from src.events import *


class GoldFromHeaven(Event):  # Gives the player a certain amount of gold... for testing? Or just fun.
    def __init__(self, player, tile, repeat, name='Gold From Heaven'):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=None)

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        print("Oddly enough, a pouch of gold materializes in front of you.")
        self.tile.spawn_item('Gold', amt=77)


class Block(Event):  # blocks exit in tile, blocks all if none are declared
    def __init__(self, player, tile, repeat, params, name='Block'):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=params)
        self.directions = []
        if not params:
            self.directions = ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']
        else:
            self.directions = params

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        for direction in self.directions:
            if direction == 'east' and 'east' not in self.tile.block_exit:
                self.tile.block_exit.append('east')
            if direction == 'west' and 'west' not in self.tile.block_exit:
                self.tile.block_exit.append('west')
            if direction == 'north' and 'north' not in self.tile.block_exit:
                self.tile.block_exit.append('north')
            if direction == 'south' and 'south' not in self.tile.block_exit:
                self.tile.block_exit.append('south')
            if direction == 'northeast' and 'northeast' not in self.tile.block_exit:
                self.tile.block_exit.append('northeast')
            if direction == 'northwest' and 'northwest' not in self.tile.block_exit:
                self.tile.block_exit.append('northwest')
            if direction == 'southeast' and 'southeast' not in self.tile.block_exit:
                self.tile.block_exit.append('southeast')
            if direction == 'southwest' and 'southwest' not in self.tile.block_exit:
                self.tile.block_exit.append('southwest')


class MakeKey(Event):  # Spawns a key for the chest with the given alias (as a param).
    def __init__(self, player, tile, repeat, params, name='MakeKey'):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=params)

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        alias = "unknown"
        name = "Key"
        desc = "A small, metal key."
        for thing in self.params:
            if '^' in thing:
                alias = thing[1:]
                continue
            if "name=" in thing:
                name = thing[5:]
                continue
            if "desc=" in thing:
                desc = thing[5:].replace('~', '.')
                continue
        lock = None
        for chest in self.player.universe.locked_chests:
            if chest[1] == alias:
                lock = chest[0]
                break
        key = self.tile.spawn_item('Key')
        key.lock = lock
        key.name = name
        key.description = desc
        key.announce = "There's a {} here.".format(key.name.lower())


class Teleport(Event):
    """
    Teleports the player to another location. Format is "t.mapname x-coord y-coord"
    """
    def __init__(self, player, tile, repeat, name='Teleport', params=None):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=None)
        self.params = params

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        for thing in self.params:
            # account for the events associated with this object. Max of 1 event.
            # Triggers after interacting with the shrine.
            if thing[0] == 't':
                param = thing.replace('t.', '')
                self.player.teleport(param)


class Shrine(Event):  # Generic class for Shrine-based events
    def __init__(self, player, tile, repeat, name='Shrine', params=None):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=None)

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        '''
        Do something! (Overwrite in subclasses)
        :return:
        '''


class StMichael(Shrine):  # Generic class for Shrine-based events
    def __init__(self, player, tile, repeat, name='Shrine of St Michael the Archangel'):
        super().__init__(name=name, player=player, tile=tile, repeat=repeat, params=None)

    def process(self):
        print("This, particularly, is a shrine to Saint Michael the Archangel.")
        print("There is a small statue depicting St Michael spearing a vicious dragon.")
        print("""An inscription on the shrine reads, 

        Sáncte Míchael Archángele, defénde nos in proélio, cóntra nequítiam et insídias diáboli ésto præsídium. 
        Ímperet ílli Déus, súpplices deprecámur: tuque, prínceps milítiæ cæléstis, Sátanam aliósque spíritus malígnos, 
        qui ad perditiónem animárum pervagántur in múndo, divína virtúte, in inférnum detrúde. Ámen.

        """)
        functions.await_input()
        print("Suddenly, Jean has the feeling of intense heat all around him. "
              "He hears a voice echoing inside his head.")
        time.sleep(2)
        cprint("""CHILD, THY FAITH PRESERVES THEE. TELL ME THE INSTRUMENT OF JUSTICE THOU DESIREST.""", "red")
        all_choices = [
            ("A crafty dagger.", "Dagger"),
            ("A trusty sword.", "Shortsword"),
            ("An imposing battleaxe.", "Battleaxe"),
            ("A useful mace.", "Mace"),
            ("A sharp pick.", "Pickaxe"),
            ("An intimidating scythe.", "Scythe"),
            ("A long spear.", "Spear"),
            ("A deadly halberd.", "Halberd"),
            ("A powerful warhammer.", "Hammer"),
            ("A reliable bow.", "Shortbow"),
            ("A convenient crossbow.", "Crossbow"),
            ("A sturdy pole.", "Pole"),
        ]
        available_choices = []
        for i in range(0, 3):
            choice = all_choices[random.randint(0, len(all_choices) - 1)]
            while choice in available_choices:
                choice = all_choices[random.randint(0, len(all_choices) - 1)]
            available_choices.append(choice)

        for i, choice in enumerate(available_choices):
            print("{}: {}".format(i, choice[0]))
        selection = input(colored("Selection: ", "cyan"))
        if functions.is_input_integer(selection):
            selection = int(selection)
        drop = self.tile.spawn_item(available_choices[selection][1], amt=1, hidden=False, hfactor=0)
        functions.add_random_enchantments(drop, 1)
        cprint("There's a brief flash of light (or was it imagined?) \nSuddenly, at the foot of the shrine, "
               "there sits a {}.".format(drop.name), "cyan")
