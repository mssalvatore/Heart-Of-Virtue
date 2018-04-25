"""
Combat states to be used within combat module. May also spill over to the standard game.
 States are objects applied to a player/npc that hang around until they expire or are removed.
"""
from termcolor import colored, cprint
import threading
import random
import time
import objects, functions


class Event: #master class for all events
    '''
    Events are added to tiles much like NPCs and items. These are evaluated each game loop to see if the conditions
    of the event are met. If so, execute the 'process' function, else pass.
    Events can also be added to the combat loop.
    Set repeat to True to automatically repeat for each game loop
    params is a list of additional parameters, None if omitted.

    '''
    def __init__(self, name, player, tile, repeat, params):
        self.name = name
        self.player = player
        self.tile = tile
        self.repeat = repeat
        self.thread = None
        self.has_run = False
        self.params = params
        self.referenceobj = None  # objects being referenced for special conditions can be put here

    def pass_conditions_to_process(self):
        self.process()
        if not self.repeat:
            if self in self.tile.events_here:
                self.tile.events_here.remove(self)  # if this is a one-time event, kill it after it executes
            elif self in self.player.combat_events:
                self.player.combat_events.remove(self)

    def check_conditions(self):
        if True:
            self.pass_conditions_to_process()

    def process(self):
        """
        to be overwritten by an event subclass
        """
        pass

    def dialogue(self, speaker, text, speaker_color="cyan", text_color="white"):
        functions.print_slow((colored(speaker+": ", speaker_color) + colored(text, text_color)), 3)
        functions.await_input()