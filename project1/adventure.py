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


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


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
        - 0 <= self.moves <= self.max_moves
    """

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    ongoing: bool
    inventory: list[str]
    score: int
    cd_player_on: bool
    usb_ejected: bool
    moves: int
    max_moves: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id
        self.ongoing = True
        self.inventory = []
        self.score = 0
        self.cd_player_on = False
        self.usb_ejected = False
        self.moves = 0
        self.max_moves = 71

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
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def display_inventory(self) -> None:
        """Display the player's inventory."""
        if self.inventory:
            print("Inventory:", ", ".join(self.inventory))
        else:
            print("Your inventory is empty.")

    def display_score(self) -> None:
        """Display the player's current score."""
        print(f"Current Score: {self.score}")

    # Constants to avoid magic numbers:
    hasan_room_id = 4
    cd_player_room_id = 3
    desk_room_id = 1
    usb_location_id = 6
    your_room_id = 1
    winning_score = 30

    def take_item(self, item_name: str) -> None:
        """Try to take an item from the current location.
        If the item is present in the location, add it to the inventory and remove it from the location.
        If the item is restricted (like the USB that must be ejected first), prevent taking it.
        """
        curr_location = self.get_location()

        if not self._can_take_item(item_name):
            return  # Prevents taking restricted items

        if item_name in curr_location.items:
            self.inventory.append(item_name)
            curr_location.items.remove(item_name)
            print(f"You have taken {item_name}.")

    def _can_take_item(self, item_name: str) -> bool:
        """Check if the item can be taken based on game rules."""
        return not (item_name == "usb" and self.current_location_id == self.usb_location_id and not self.usb_ejected)

    def use_item(self, item_name: str) -> None:
        """Use an item from the inventory."""
        curr_location = self.get_location()
        hasan_room = self._locations.get(self.hasan_room_id)

        if item_name.lower() not in (i.lower() for i in self.inventory):
            print("You do not have that item.")
            return

        item_obj = next((item for item in self._items if item.name.lower() == item_name.lower()), None)
        if not item_obj:
            print("Error: Item not found in game data.")
            return

        if self._can_use_item(item_name, curr_location, hasan_room):
            self.score += item_obj.target_points
        else:
            print("You cannot use this item here.")

    def _can_use_item(self, item_name: str, curr_location: Location, hasan_room: Location) -> bool:
        """Check if an item can be used in the current location and perform the action if possible."""
        if item_name == "lockpick" and curr_location.id_num in {20, 21} and hasan_room.locked:
            hasan_room.locked = False
            print("You successfully unlocked Hasan's Room with the lockpick!")
            return True
        if item_name == "batteries" and curr_location.id_num == self.cd_player_room_id:
            self.cd_player_on = True
            print("You inserted the batteries into the CD player. It is now on!")
            return True
        if item_name == "movie cd":
            return self._handle_movie_cd(curr_location)
        if item_name in {"lucky uoft mug", "laptop charger", "usb"} and curr_location.id_num == self.desk_room_id:
            return self._handle_special_items(item_name)

        return False  # Item could not be used

    def _handle_movie_cd(self, curr_location: Location) -> bool:
        """Handle the usage of the movie CD."""
        if curr_location.id_num == self.cd_player_room_id and self.cd_player_on:
            print("The CD player starts playing: Madagascar!")
            return True
        if curr_location.id_num == self.cd_player_room_id and not self.cd_player_on:
            print("You must turn on the CD player first, you need some batteries...")
            return False
        return False

    def _handle_special_items(self, item_name: str) -> bool:
        """Handle items that contribute to the win condition."""
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

    def attempt_usb_retrieval(self) -> None:
        """Handle the process of safely retrieving the USB in the Library."""
        if self.current_location_id != 6:
            print("There's nothing to do here.")
            return

        if self.usb_ejected:
            print("The USB has been safely ejected. You can take it now.")
            return

        # Prompt for password to eject USB
        print(
            "The computer warns: 'If you unplug it normally, it might corrupt. You may want to manually eject "
            "it first, but you need to sign in.'")
        print("Hint: No caps, no spaces, no special characters. Favorite movie + birthday")

        if input("Enter password: ") == "madagascar05252006":
            self.usb_ejected = True
            print("You have safely ejected the USB. You can now take it.")
        else:
            print("Incorrect password. Try again later.")

    def check_win_condition(self) -> bool:
        """Check if the player has met the winning condition."""
        if self.current_location_id == self.your_room_id and self.score == self.winning_score:
            print("\n🎉 Congratulations! You successfully submitted your assignment and won, you scored 100%! 🎉\n")
            self.ongoing = False
            return True

    def process_menu_action(self, user_choice: str, log: EventList) -> None:
        """Handle menu actions like inventory, score, log, quit, and undo."""
        if user_choice == "log":
            log.display_events()
        elif user_choice == "quit":
            self.ongoing = False
        elif user_choice == "undo":
            if self.moves >= 2:
                self.moves -= 2
            log.remove_last_event()
            self.current_location_id = log.last.id_num if log.last else 1
        elif choice == "inventory":
            self.display_inventory()
        elif choice == "score":
            self.display_score()
        elif choice == "look":
            print(self.get_location().long_description)

    def handle_take_or_use(self, user_choice: str) -> None:
        """Process 'take' and 'use' commands."""
        if user_choice.startswith("take "):
            self.take_item(user_choice[len("take "):])
        elif user_choice.startswith("use "):
            self.use_item(user_choice[len("use "):])

    def handle_special_actions(self, user_choice: str, loc: Location) -> None:
        """Handle special commands for specific locations (e.g., retrieving USB)."""
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
    game_log = EventList()
    game = AdventureGame('game_data.json', 1)
    menu = ["look", "inventory", "score", "undo", "log", "quit", "take", "use"]
    choice = None

    while game.ongoing:
        if game.check_win_condition() is True:
            break
        location = game.get_location()
        event = Event(game.current_location_id, location.brief_description, choice)
        game_log.add_event(event)
        game.moves += 1
        print(f"Moves remaining: {game.max_moves - game.moves}")

        if game.moves >= game.max_moves:
            print("\nYou ran out of time! You failed to submit your assignment. Game Over.")
            game.ongoing = False
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
