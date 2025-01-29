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
from typing import Optional, Dict, List

from game_entities import Location, Item, Puzzle
from proj1_event_logger import Event, EventList

# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations: a mapping from location id to Location object.
        - _items: a dictionary of Item objects, representing all items in the game.
        - _puzzles: a dictionary mapping puzzle names to Puzzle objects.
        - _inventory: a list of items currently held by the player.
        - current_location_id: The ID of the player's current location.
        - ongoing: Whether the game is ongoing.
        - score: The player's score based on completed objectives.
    """
    _locations: dict[int, Location]
    _items: dict[str, Item]
    _puzzles: dict[str, Puzzle]
    _inventory: List[str]
    current_location_id: int
    ongoing: bool
    score: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        """
        self._locations, self._items, self._puzzles = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id
        self.ongoing = True
        self._inventory = []  # Start with an empty inventory
        self.score = 0  # Initialize score to zero

    @staticmethod
    def _load_game_data(filename: str) -> tuple[Dict[int, Location], Dict[str, Item], Dict[str, Puzzle]]:
        """Load game locations, items, and puzzles from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)

        locations = {
            loc_data['id']: Location(
                id_num=loc_data['id'],
                brief_description=loc_data['brief_description'],
                long_description=loc_data.get('long_description', ''),
                available_commands=loc_data.get('available_commands', {}),
                items=loc_data.get('items', []),
                locked=loc_data.get('locked', False),
                visited=False
            )
            for loc_data in data['locations']
        }

        items = {
            item_data['name']: Item(
                name=item_data['name'],
                description=item_data['description'],
                start_position=item_data['start_position'],
                target_position=item_data.get('target_position', None),
                target_points=item_data.get('target_points', 0)
            )
            for item_data in data['items']
        }

        puzzles = {
            puzzle_name: Puzzle(
                name=puzzle_name,
                description=puzzle_data['description'],
                required_items=puzzle_data['required_items'],
                solution=puzzle_data['solution']
            )
            for puzzle_name, puzzle_data in data.get('puzzles', {}).items()
        }

        return locations, items, puzzles

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        return self._locations[loc_id if loc_id is not None else self.current_location_id]

    def pick_up_item(self, item_name: str) -> None:
        """Allow the player to pick up an item if it is in the current location."""
        location = self.get_location()
        if item_name in location.items:
            self._inventory.append(item_name)
            location.items.remove(item_name)
            print(f"You picked up {item_name}.")
        else:
            print("You can't pick that up.")

    def use_item(self, item_name: str) -> None:
        """Allow the player to use an item if it's in their inventory."""
        if item_name in self._inventory:
            print(f"You used {item_name}.")
            self._inventory.remove(item_name)
        else:
            print("You don't have that item.")

    def check_score(self) -> None:
        """Display the player's current score."""
        print(f"Your score is: {self.score}")


if __name__ == "__main__":
    game_log = EventList()
    game = AdventureGame('game_data.json', 1)
    menu = ["look", "inventory", "score", "undo", "log", "quit"]
    choice = None

    while game.ongoing:
        location = game.get_location()
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
        print("========")
        print("You decided to:", choice)
        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "inventory":
                print("Inventory:", game._inventory)
            elif choice == "score":
                game.check_score()
        else:
            result = location.available_commands[choice]
            game.current_location_id = result
