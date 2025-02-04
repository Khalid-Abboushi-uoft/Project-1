"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


class GameState:
    """Represents the current state of the adventure game.

    Attributes:
        ongoing (bool): A flag indicating whether the game is still in progress.
        score (int): The player's current score.
        moves (int): The number of moves the player has taken so far.
        max_moves (int): The maximum number of moves allowed before the game ends.
    """
    ongoing: bool
    score: int
    moves: int
    max_moves: int

    def __init__(self) -> None:
        """
        Initialize all game state variables
        """
        self.ongoing = True
        self.score = 0
        self.moves = 0
        self.max_moves = 71


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations: A dictionary mapping location IDs to Location objects.
        - _items: A list of all Item objects present in the game.
        - current_location_id: The ID of the player's current location.
        - ongoing: A boolean indicating whether the game is still in progress.
        - inventory: A list of items currently in the player's possession.
        - score: The player's current score.
        - cd_player_on: Whether the CD player in Khalid's Room is on.
        - usb_ejected: Whether the USB has been safely ejected from the computer.

    Representation Invariants:
        - current_location_id in self._locations
        - all(isinstance(loc, Location) for loc in self._locations.values())
        - all(isinstance(item, Item) for item in self._items)
    """

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    inventory: list[str]
    cd_player_on: bool
    usb_ejected: bool
    game_state: GameState

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        self._locations, self._items = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id
        self.inventory = []
        self.cd_player_on = False
        self.usb_ejected = False
        self.game_state = GameState()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data.get('long_description', None), loc_data['available_commands'],
                                    loc_data.get('items', []), loc_data.get('locked', False),
                                    loc_data.get('visited', False), loc_data.get('special_commands'))
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """
        Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game._locations[1] = Location(1, "Starting Room", "A quiet starting place.", None, {}, [], False, False, {})
        >>> game._locations[2] = Location(2, "Hallway", "A long hallway.", None, {}, [], False, False, {})

        >>> game.current_location_id = 1
        >>> loc = game.get_location()
        >>> loc.id_num, loc.name
        (1, 'Starting Room')

        >>> loc = game.get_location(2)
        >>> loc.id_num, loc.name
        (2, 'Hallway')
        """

        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def display_inventory(self) -> None:
        """
        Display the player's inventory.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.inventory = []
        >>> game.display_inventory()
        Your inventory is empty.

        >>> game.inventory = ["key"]
        >>> game.display_inventory()
        Inventory: key

        >>> game.inventory = ["key", "flashlight", "map"]
        >>> game.display_inventory()
        Inventory: key, flashlight, map
        """

        if self.inventory:
            print("Inventory:", ", ".join(self.inventory))
        else:
            print("Your inventory is empty.")

    def display_score(self) -> None:
        """
        Display the player's current score.

        >>> game = AdventureGame('game_data.json', 1)  # Initialize game
        >>> game.game_state.score = 0
        >>> game.display_score()
        Current Score: 0

        >>> game.game_state.score = 15
        >>> game.display_score()
        Current Score: 15

        >>> game.game_state.score = 30
        >>> game.display_score()
        Current Score: 30
        """

        print(f"Current Score: {self.game_state.score}")

    def take_item(self, item_name: str) -> None:
        """
        Check if the item can be taken based on game rules.

        >>> game = AdventureGame('game_data.json', 6)  # Start in the Library (location 6)
        >>> game.usb_ejected = False
        >>> game._can_take_item("usb")
        False

        >>> game.usb_ejected = True
        >>> game._can_take_item("usb")
        True

        >>> game.current_location_id = 5  # Change location to a non-restricted area
        >>> game._can_take_item("usb")
        True

        >>> game._can_take_item("book")  # Any other item should be allowed
        True
        """

        curr_location = self.get_location()

        if not self._can_take_item(item_name):
            return  # Prevents taking restricted items

        if item_name in curr_location.items:
            self.inventory.append(item_name)
            curr_location.items.remove(item_name)
            print(f"You have taken {item_name}.")

    def _can_take_item(self, item_name: str) -> bool:
        """
        Check if the item can be taken based on game rules.

        >>> game = AdventureGame('game_data.json', 6)  # Start in the Library (location 6)
        >>> game.usb_ejected = False
        >>> game._can_take_item("usb")
        False

        >>> game.usb_ejected = True
        >>> game._can_take_item("usb")
        True

        >>> game.current_location_id = 5  # Change location to a non-restricted area
        >>> game._can_take_item("usb")
        True

        >>> game._can_take_item("book")  # Any other item should be allowed
        True
        """

        usb_location_id = 6
        return not (item_name == "usb" and self.current_location_id == usb_location_id and not self.usb_ejected)

    def use_item(self, item_name: str) -> None:
        """
        Use an item from the inventory.

        >>> game = AdventureGame('game_data.json', 1)  # Start in the desk room
        >>> game.inventory = ["laptop charger", "usb", "lockpick"]  # Add items to inventory
        >>> desk_location = Location(1, "Desk Room", "A room with a desk.", None, {}, [], False, False, {})
        >>> hasan_room = Location(4, "Hasan's Room", "A locked room.", None, {}, [], True, False, {})

        >>> game._locations[1] = desk_location
        >>> game._locations[4] = hasan_room

        >>> game.use_item("laptop charger")
        You plugged in your laptop charger. Your laptop is now charging.

        >>> game.use_item("usb")
        You plugged the USB into your computer.

        >>> game.use_item("lockpick")  # Should fail since we're not in the correct location
        You cannot use this item here.

        >>> game.use_item("random item")  # Not in inventory
        You do not have that item.
        """

        hasan_room_id = 4
        curr_location = self.get_location()
        hasan_room = self._locations.get(hasan_room_id)

        if item_name.lower() not in (i.lower() for i in self.inventory):
            print("You do not have that item.")
            return

        item_obj = next((item for item in self._items if item.name.lower() == item_name.lower()), None)
        if not item_obj:
            print("Error: Item not found in game data.")
            return

        if self._can_use_item(item_name, curr_location, hasan_room):
            self.game_state.score += item_obj.target_points
        else:
            print("You cannot use this item here.")

    def _can_use_item(self, item_name: str, curr_location: Location, hasan_room: Location) -> bool:
        """
        Check if an item can be used in the current location and perform the action if possible.

        >>> game = AdventureGame('game_data.json', 1)  # Start in the desk room
        >>> desk_location = Location(1, "Desk Room", "A room with a desk.", None, {}, [], False, False, {})
        >>> hasan_location = Location(4, "Hasan's Room", "A locked room.", None, {}, [], True, False, {})

        >>> game._can_use_item("lucky uoft mug", desk_location, hasan_location)
        You placed the Lucky UofT Mug on the desk beside your computer.
        True

        >>> game._can_use_item("laptop charger", desk_location, hasan_location)
        You plugged in your laptop charger. Your laptop is now charging.
        True

        >>> game._can_use_item("usb", desk_location, hasan_location)
        You plugged the USB into your computer.
        True
        """

        cd_player_room_id = 3
        desk_room_id = 1
        if item_name == "lockpick" and curr_location.id_num in {20, 21} and hasan_room.locked:
            hasan_room.locked = False
            print("You successfully unlocked Hasan's Room with the lockpick!")
            return True
        if item_name == "batteries" and curr_location.id_num == cd_player_room_id:
            self.cd_player_on = True
            print("You inserted the batteries into the CD player. It is now on!")
            return True
        if item_name == "movie cd":
            return self._handle_movie_cd(curr_location)
        if item_name in {"lucky uoft mug", "laptop charger", "usb"} and curr_location.id_num == desk_room_id:
            return self._handle_special_items(item_name)

        return False  # Item could not be used

    def _handle_movie_cd(self, curr_location: Location) -> bool:
        """
        Handle the usage of the movie CD.

        >>> game = AdventureGame('game_data.json', 3)  # Start in the CD player room
        >>> location = Location(3, "CD Player Room", "A room with a CD player.", None, {}, [], False, False, {})

        >>> game.cd_player_on = False
        >>> game._handle_movie_cd(location)
        You must turn on the CD player first, you need some batteries...
        False

        >>> game.cd_player_on = True
        >>> game._handle_movie_cd(location)
        The CD player starts playing: Madagascar!
        True

        >>> other_location = Location(2, "Another Room", "A random location.", None, {}, [], False, False, {})
        >>> game._handle_movie_cd(other_location)  # Not in the CD player room
        False
        """

        cd_player_room_id = 3
        if curr_location.id_num == cd_player_room_id and self.cd_player_on:
            print("The CD player starts playing: Madagascar!")
            return True
        if curr_location.id_num == cd_player_room_id and not self.cd_player_on:
            print("You must turn on the CD player first, you need some batteries...")
            return False
        return False

    def _handle_special_items(self, item_name: str) -> bool:
        """
        Handle items that contribute to the win condition.

        >>> game = AdventureGame('game_data.json', 1)  # Start in the player's room
        >>> game._handle_special_items("lucky uoft mug")
        You placed the Lucky UofT Mug on the desk beside your computer.
        True

        >>> game._handle_special_items("laptop charger")
        You plugged in your laptop charger. Your laptop is now charging.
        True

        >>> game._handle_special_items("usb")
        You plugged the USB into your computer.
        True

        >>> game._handle_special_items("random item")  # Item not in special_items
        False
        """

        special_items = {
            "lucky uoft mug": "You placed the Lucky UofT Mug on the desk beside your computer.",
            "laptop charger": "You plugged in your laptop charger. Your laptop is now charging.",
            "usb": "You plugged the USB into your computer."
        }

        if item_name in special_items:
            print(special_items[item_name])
            self.check_win_condition()
            return True
        return False

    def attempt_usb_retrieval(self, password: str = None) -> None:
        """
        Handle the process of safely retrieving the USB in the Library.

        >>> game = AdventureGame('game_data.json', 6)  # Start in the Library
        >>> game.usb_ejected = False
        >>> game.attempt_usb_retrieval("wrongpassword")
        The computer warns: 'If you unplug it normally, it might corrupt. You may want to manually eject
        it first, but you need to sign in.'
        Hint: No caps, no spaces, no special characters. Favorite movie + birthday
        Incorrect password. Try again later.

        >>> game.attempt_usb_retrieval("madagascar05252006")
        The computer warns: 'If you unplug it normally, it might corrupt. You may want to manually eject
        it first, but you need to sign in.'
        Hint: No caps, no spaces, no special characters. Favorite movie + birthday
        You have safely ejected the USB. You can now take it.

        >>> game.usb_ejected  # Ensure the USB is ejected
        True
        """

        if self.current_location_id != 6:
            print("There's nothing to do here.")
            return

        if self.usb_ejected:
            print("The USB has been safely ejected. You can take it now.")
            return

        print("The computer warns: 'If you unplug it normally, it might corrupt. You may want to manually eject\n"
              "it first, but you need to sign in.'")
        print("Hint: No caps, no spaces, no special characters. Favorite movie + birthday")

        if password is None:  # Allow real input in gameplay
            password = input("Enter password: ")

        if password == "madagascar05252006":
            self.usb_ejected = True
            print("You have safely ejected the USB. You can now take it.")
        else:
            print("Incorrect password. Try again later.")

    def check_win_condition(self) -> bool:
        """
        Check if the player has met the winning condition.

        >>> game = AdventureGame('game_data.json', 1)  # Initialize game at room 1
        >>> game.game_state.score = 30
        >>> game.check_win_condition()
        <BLANKLINE>
        🎉 Congratulations! You successfully submitted your assignment and won, you scored 100%! 🎉
        <BLANKLINE>
        True

        >>> game = AdventureGame('game_data.json', 1)  # Reinitialize game
        >>> game.game_state.score = 25  # Score is below winning threshold
        >>> game.check_win_condition()
        False

        >>> game = AdventureGame('game_data.json', 2)  # Player is not in room 1
        >>> game.game_state.score = 30
        >>> game.check_win_condition()
        False
        """

        your_room_id = 1
        winning_score = 30
        if self.current_location_id == your_room_id and self.game_state.score == winning_score:
            print("\n🎉 Congratulations! You successfully submitted your assignment and won, you scored 100%! 🎉\n")
            self.game_state.ongoing = False
            return True
        return False

    def process_menu_action(self, user_choice: str, log: EventList) -> None:
        """
        Handle menu actions like inventory, score, log, quit, and undo.

        >>> game = AdventureGame('game_data.json', 1)  # Initialize game
        >>> log = EventList()

        >>> game.process_menu_action("quit", log)
        >>> game.game_state.ongoing
        False

        >>> game.process_menu_action("inventory", log)
        Your inventory is empty.

        >>> game.game_state.moves = 3  # Simulate game progress
        >>> game.process_menu_action("undo", log)

        >>> game.game_state.moves  # Should be reduced by 2
        1
        """

        if user_choice == "log":
            log.display_events()
        elif user_choice == "quit":
            self.game_state.ongoing = False
        elif user_choice == "undo":
            if self.game_state.moves >= 2:
                self.game_state.moves -= 2
            log.remove_last_event()
            self.current_location_id = log.last.id_num if log.last else 1
        elif user_choice == "inventory":
            self.display_inventory()
        elif user_choice == "score":
            self.display_score()
        elif user_choice == "look":
            print(self.get_location().long_description)

    def handle_take_or_use(self, user_choice: str) -> None:
        """
        Process 'take' and 'use' commands in the adventure game.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game._locations[1] = Location(1, "Room", "A small room.", None, {}, ["key"], False, False, [])

        >>> game.handle_take_or_use("take key")
        You have taken key.

        >>> game.inventory.append("flashlight")
        >>> game.handle_take_or_use("use flashlight")
        Error: Item not found in game data.

        >>> game.handle_take_or_use("use battery")
        You do not have that item.
        """

        if user_choice.startswith("take "):
            self.take_item(user_choice[len("take "):])
        elif user_choice.startswith("use "):
            self.use_item(user_choice[len("use "):])

    def handle_special_actions(self, user_choice: str, loc: Location) -> None:
        """
        Handle special commands for specific locations (e.g., retrieving USB or unlocking doors).

        >>> game = AdventureGame('game_data.json', 6)
        >>> game.handle_special_actions("take usb", game.get_location(6))
        You cannot take the USB drive until you safely eject it.

        >>> game.usb_ejected = True
        >>> game.handle_special_actions("take usb", game.get_location(6))
        You have taken usb.
        """
        library_room_id = 6
        hasan_room_id = 4
        if self.current_location_id == library_room_id and user_choice == "take usb":
            if self.usb_ejected:
                self.take_item("usb")
            else:
                print("You cannot take the USB drive until you safely eject it.")
        elif self.current_location_id == library_room_id and choice == "retrieve usb":
            self.attempt_usb_retrieval()
        elif user_choice in loc.available_commands:
            next_location_id = loc.available_commands[user_choice]
            next_location = self.get_location(next_location_id)
            if next_location_id == hasan_room_id and getattr(next_location, 'locked', False):
                print("The door is locked. You need something to unlock it.")
            else:
                self.current_location_id = next_location_id


if __name__ == "__main__":
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
    game_log = EventList()
    game = AdventureGame('game_data.json', 1)
    menu = ["look", "inventory", "score", "undo", "log", "quit", "take", "use"]
    choice = None

    while game.game_state.ongoing:
        if game.check_win_condition() is True:
            break
        location = game.get_location()
        event = Event(game.current_location_id, location.brief_description, choice)
        game_log.add_event(event)
        game.game_state.moves += 1
        print(f"Moves remaining: {game.game_state.max_moves - game.game_state.moves}")

        if game.game_state.moves >= game.game_state.max_moves:
            print("\nYou ran out of time! You failed to submit your assignment. Game Over.")
            game.game_state.ongoing = False
            break

        print(location.brief_description if location.visited or location.long_description is None
              else location.long_description)
        location.visited = True

        print("What to do? Choose from:", ", ".join(menu))
        for action in list(location.available_commands.keys()) + location.special_commands:
            print("-", action)

        choice = input("\nEnter action: ").lower().strip()
        while (choice not in location.available_commands and choice not in menu
               and choice not in location.special_commands
               and not choice.startswith("take ") and not choice.startswith("use ")):
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("=========================")
        print("You decided to:", choice)

        if choice in menu:
            game.process_menu_action(choice, game_log)
        else:
            game.handle_take_or_use(choice)
            game.handle_special_actions(choice, location)
