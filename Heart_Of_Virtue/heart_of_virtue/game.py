"""
My take on Phillip Johnson's text adventure tutorial
"""
__author__ = 'Alex Egbert'
import world, functions, intro_scene
from player import Player
from termcolor import colored

print_slow = functions.print_slow
screen_clear = functions.screen_clear
def play():
    world.load_tiles()
    world.place_enemies() #loads the default enemies into world tiles
    world.place_items() #same thing for items
    player = Player()
    room = world.tile_exists(player.location_x, player.location_y)
    functions.test_color()
    # intro_scene.intro() # Comment this out to disable the intro sequence
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        player.current_room = room
        room.modify_player(player)
        functions.check_for_enemies(room)
        functions.check_for_items(room)
        combat_list = functions.check_for_combat(player)
        if len(combat_list) > 0:
            print(colored("You ready yourself for battle!","red")) #todo: initiate combat loop



        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            # Check the state of the room to see if there are any enemies

            print("Choose an action:\n")
            available_actions = room.adjacent_moves()
            print('| ',end='')
            for action in available_actions:
                print(action, end=' | ')
            print("\n\nFor a list of additional commands, enter 'c'.\n")
            action_input = input('Action: ')
            available_actions = room.available_actions()
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break



if __name__ == "__main__":
    play()