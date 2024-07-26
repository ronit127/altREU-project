from typing import List

class Node:

    # node contains name(string), skills(list of strings), difficulty(double)
    def __init__(self, key: int, name: str, skills: List[str], difficulty: float) -> None:
        self.name = name
        self.skills = skills
        self.difficulty = difficulty
        self.key = key

