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
    """

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    ongoing: bool
    inventory: list[str]
    score: int
    cd_player_on: bool
    usb_ejected: bool

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

    def take_item(self, item_name: str) -> None:
        """Take an item from the current location."""
        curr_location = self.get_location()
        if item_name in curr_location.items:
            self.inventory.append(item_name)
            curr_location.items.remove(item_name)
            print(f"You have taken {item_name}.")
        else:
            print("There is no such item here.")

    def use_item(self, item_name: str) -> None:
        """Use an item from the inventory."""
        curr_location = self.get_location()
        if item_name in self.inventory:
            if item_name == "lockpick" and curr_location.id_num == 4 and curr_location.locked:
                curr_location.locked = False
                print("You successfully unlocked Hasan's Room with the lockpick!")
            elif item_name == "Batteries" and curr_location.id_num == 3:
                self.cd_player_on = True
                print("You inserted the batteries into the CD player. It is now on!")
            elif item_name == "Movie CD" and curr_location.id_num == 3 and self.cd_player_on:
                print("The CD player starts playing: Madagascar!")
            elif item_name == "Lucky UofT Mug" and curr_location.id_num == 1:
                print("You placed the Lucky UofT Mug on the desk beside your computer.")
            elif item_name == "Laptop charger" and curr_location.id_num == 1:
                print("You plugged in your laptop charger. Your laptop is now charging.")
            else:
                print("You cannot use this item here.")
        else:
            print("You do not have that item.")

    def attempt_usb_retrieval(self) -> None:
        """Handle the process of safely retrieving the USB in the Library."""
        if self.current_location_id == 6 and not self.usb_ejected:
            print(
                "The computer warns: 'If you unplug it normally, it might corrupt. You may want to manually eject "
                "it first, but you need to sign in.'")
            print("Hint: No caps, no spaces, no special characters. Favorite movie + birthday")
            password = input("Enter password: ")
            if password == "madagascar05252006":
                self.usb_ejected = True
                print("You have safely ejected the USB. You can now take it.")
            else:
                print("Incorrect password. Try again later.")
        elif self.current_location_id == 6 and self.usb_ejected:
            print("The USB has been safely ejected. You can take it now.")
        else:
            print("There's nothing to do here.")


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit", "take", "use"]  # Regular menu options available
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # Add new Event to game log
        event = Event(game.current_location_id, location.brief_description, choice)
        game_log.add_event(event)

        # Print location description
        if location.visited or location.long_description is None:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit, take, use")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        for command in location.special_commands:
            print("-", command)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and choice not in location.special_commands:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("=========================")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "quit":
                game.ongoing = False
            elif choice == "undo":
                game_log.remove_last_event()
                if game_log.last:
                    game.current_location_id = game_log.last.id_num
                else:
                    game.current_location_id = 1  # Reset to starting location if no previous events
            elif choice == "inventory":
                game.display_inventory()
            elif choice == "score":
                game.display_score()
            elif choice == "look":
                print(game.get_location().long_description)

        else:
            if game.current_location_id == 6 and choice == "take usb":
                # Check if USB is safely ejected before allowing the player to take it
                if game.usb_ejected:
                    game.take_item("usb")  # Allow the player to take the USB
                else:
                    print("You cannot take the USB drive until you safely eject it.")

            elif game.current_location_id == 6 and choice == "retrieve usb":
                # Library USB puzzle (eject USB safely)
                game.attempt_usb_retrieval()

            elif choice in location.available_commands:
                # Check if the player is trying to enter Hasan's Room (ID 4)
                next_location_id = location.available_commands[choice]
                next_location = game.get_location(next_location_id)  # Retrieve the next location object

                if next_location_id == 4 and getattr(next_location, 'locked', False):
                    print("The door is locked. You need something to unlock it.")
                else:
                    # Move to the new location
                    game.current_location_id = next_location_id

            else:
                print("You can't do that here.")
