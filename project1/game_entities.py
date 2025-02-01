"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
the `adventure` module.
Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""

from typing import Optional


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique ID of this location (must be > 0)
        - name: The name of this location
        - brief_description: A short description of the location
        - long_description: A detailed description of the location
        - available_commands: A dictionary mapping commands (e.g., 'go east') to location IDs
        - items: A list of item names available at this location
        - locked: Whether this location is locked and requires an item to unlock
        - visited: Whether this location has been visited before
        - special_commands: Special actions a player can take in this location

    Representation Invariants:
        - self.id_num > 0
    """

    id_num: int
    name: str
    brief_description: str
    long_description: Optional[str]
    available_commands: dict[str, int]
    items: list[str]
    locked: bool
    visited: bool
    special_commands: list[str]

    def __init__(self, id_num: int, name: str, brief_description: str, long_description: Optional[str] = None,
                 available_commands: Optional[dict[str, int]] = None, items: Optional[list[str]] = None,
                 locked: bool = False, visited: bool = False, special_commands: Optional[list[str]] = None) -> None:
        """Initialize a new location."""
        self.id_num = id_num
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands if available_commands else {}
        self.items = items if items else []
        self.locked = locked
        self.visited = visited
        self.special_commands = special_commands if special_commands else []


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item
        - description: A short description of the item
        - start_position: The ID of the location where this item starts (must be > 0)
        - target_position: The ID of the location where this item should be returned (if applicable, must be > 0)
        - target_points: The number of points this item contributes if placed correctly

    Representation Invariants:
        - self.start_position > 0
        - self.target_position is None or self.target_position > 0
    """

    name: str
    description: str
    start_position: int
    target_position: Optional[int]
    target_points: int

    def __init__(self, name: str, description: str, start_position: int, target_position: Optional[int],
                 target_points: int) -> None:
        """Initialize a new item."""
        self.name = name
        self.description = description
        self.start_position = start_position
        self.target_position = target_position
        self.target_points = target_points


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'R0913']
    })
