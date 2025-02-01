"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location
from dataclasses import dataclass
import json
from typing import Optional


# Note: We have completed the Location class for you. Do NOT modify it here, for ex1.
@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - description: brief description of this location
        - available_commands: a mapping of available commands at this location to
                                the location executing that command would lead to
    """
    id_num: int
    description: str
    available_commands: dict[str, int]


class SimpleAdventureGame:
    """A simple text adventure game class storing all location data.

    Instance Attributes:
        - current_location_id: the ID of the location the game is currently in
    """

    # Private Instance Attributes:
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    _locations: dict[int, Location]
    current_location_id: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file.

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # Note: We have completed this method for you. Do NOT modify it here, for ex1.

        self._locations = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id  # game begins at this location

    @staticmethod
    def _load_game_data(filename: str) -> dict[int, Location]:
        """Load locations and items from a JSON file with the given filename and
        return a dictionary of locations mapping each game location's ID to a Location object."""

        # Note: We have completed this method for you. Do NOT modify it here, for ex1.

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['long_description'], loc_data['available_commands'])
            locations[loc_data['id']] = location_obj

        return locations

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: SimpleAdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.
        """
        self._events = EventList()
        self._game = SimpleAdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        first_event = Event(initial_location.id_num, initial_location.description, None)
        self._events.add_event(first_event)

        # Generate the remaining events
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.
        """
        for command in commands:
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id)

                # Create new event and add to the event list
                new_event = Event(next_location.id_num, next_location.description, command)
                self._events.add_event(new_event, command)

                # Update current location
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # TODO: Modify the code below to provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = [
        "look", "go east", "go east", "go east", "go east", "go south", "go east", "go east", "look",
        "take lockpick", "go west", "go west", "go west", "go west", "use lockpick", "go west",
        "take movie cd", "go east", "go south", "go south", "go west", "go west", "look",
        "take lucky uoft mug", "take batteries", "go east", "go east", "go south", "go south",
        "go south", "look", "take laptop charger", "go north", "go north", "go north", "go north",
        "go north", "go north", "use batteries", "use movie cd", "go east", "go east",
        "go south", "go east", "go east", "retrieve usb", "madagascar05252006", "take usb",
        "go west", "go west", "go west", "go west", "go north", "go west",
        "use usb", "use laptop charger", "use lucky uoft mug"
    ]
    expected_log = ["1", "20", "3", "22", "52", "51", "53", "6", "50", "21", "4", "57", "58", "59", "60", "61", "8", "7"]

    # Uncomment the line below to test your walkthrough
    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough)

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = []
    expected_log = []  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your demo
    assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo)

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    # inventory_demo = [..., "inventory", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # scores_demo = [..., "score", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Note: You can add more code below for your own testing purposes
