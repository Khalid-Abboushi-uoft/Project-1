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


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        first_event = Event(initial_location.id_num, initial_location.long_description, None)
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
                new_event = Event(next_location.id_num, next_location.long_description, command)
                self._events.add_event(new_event, command)

                # Update current location
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 20]
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
    expected_log = [1, 20, 3, 22, 52, 51, 53, 6, 53, 51, 50, 21, 4, 21,
                    57, 58, 61, 7, 61, 58, 59, 60, 8, 60, 59, 58, 57, 21,
                    3, 22, 52, 51, 53, 6, 53, 51, 50, 21, 3, 20
                    ]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough).get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    # lose_demo = ['look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look',
    #              'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look',
    #              'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look',
    #              'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look',
    #              'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look',
    #              'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look', 'look']
    # expected_log = [1]
    # Uncomment the line below to test your demo
    # assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo).get_id_log()

    # inventory_demo = ["go east", "go east", "go south", "go south", "go south", "go west", "go west",
    #                   "take batteries", "take lucky uoft mug", "inventory"]
    # expected_log = [1, 20, 3, 21, 57, 58, 61, 7]
    # assert expected_log == AdventureGameSimulation('game_data.json', 1, inventory_demo).get_id_log()

    # scores_demo = ["go east", "go east", "go south", "go south", "go south", "go west", "go west",
    #                "take lucky uoft mug", "go east", "go east", "go north", "go north", "go north", "go west",
    #                "go west", "use lucky uoft mug", "score"]
    # expected_log = [1, 20, 3, 21, 57, 58, 61, 7, 61, 58, 57, 21, 3, 20, 1]
    # assert expected_log == AdventureGameSimulation('game_data.json', 1, scores_demo).get_id_log()

    # retrieve_usb_demo = ["go east", "go east", "go east", "go east", "go south", "go east", "go east", "retrieve_usb",
    #                      "madagascar05252006"]
    # expected_log = [1, 20, 3, 22, 52, 51, 53, 6]
    # assert expected_log == AdventureGameSimulation('game_data.json', 1, retrieve_usb_demo).get_id_log()
