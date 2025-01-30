"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


# TODO: Copy/paste your x1_event_logeger code below, and modify it if needed to fit your game


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    id_num: int
    description: str
    next_command: Optional[str]
    next: Optional['Event'] = None
    prev: Optional['Event'] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first event in the linked list, or None if the list is empty
        - last: The last event in the linked list, or None if the list is empty
    Representation Invariants:
        - self.first is None == self.last is None  # If first is None, last must also be None
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.event_log = []

    def display_events(self) -> None:
        """Display all events in chronological order."""
        print("Event Log:")
        for i, event in enumerate(self.event_log, 1):
            print(f"{i}. {event}")

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        return self.first is None

    def add_event(self, event: Event, command: Optional[str] = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        if self.last is None:
            # If the list is empty, set both first and last to the new event
            self.first = event
        else:
            # Otherwise, link the new event to the last event
            self.last.next = event
            event.prev = self.last
            self.last.next_command = command  # Update the previous node's next_command

            # Update last to the new event
        self.last = event

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing.
        """
        if self.is_empty():
            return  # List is empty, do nothing

        if self.first == self.last:
            # Only one event in the list, remove it
            self.first = None
            self.last = None
        else:
            # Update the last event to be the previous event
            self.last = self.last.prev
            if self.last:
                self.last.next = None
                self.last.next_command = None  # Remove the command leading to the removed event

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        id_log = []
        curr = self.first

        while curr:
            id_log.append(curr.id_num)
            curr = curr.next

        return id_log

    # Note: You may add other methods to this class as needed but DO NOT CHANGE THE SPECIFICATION OF ANY OF THE ABOVE


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
