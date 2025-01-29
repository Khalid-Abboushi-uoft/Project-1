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
from dataclasses import dataclass


from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique ID of this location
        - brief_description: A short description of the location
        - long_description: A detailed description of the location
        - available_commands: A dictionary mapping commands (e.g., 'go east') to location IDs
        - items: A list of item names available at this location
        - locked: Whether this location is locked and requires an item to unlock
        - visited: Whether this location has been visited before

    Representation Invariants:
        - id_num > 0
    """
    id_num: int
    brief_description: str
    long_description: str
    available_commands: Dict[str, int]
    items: List[str]
    locked: bool = False
    visited: bool = False

@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item
        - description: A short description of the item
        - start_position: The ID of the location where this item starts
        - target_position: The ID of the location where this item should be returned (if applicable)
        - target_points: The number of points this item contributes if placed correctly
    """
    name: str
    description: str
    start_position: int
    target_position: Optional[int]
    target_points: int

@dataclass
class Puzzle:
    """A puzzle in our text adventure game world.

    Instance Attributes:
        - name: The name of the puzzle
        - description: A short description of the puzzle
        - required_items: A list of items required to solve the puzzle
        - solution: The correct solution to the puzzle
        - solved: Whether the puzzle has been solved
    """
    name: str
    description: str
    required_items: List[str]
    solution: str
    solved: bool = False


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
