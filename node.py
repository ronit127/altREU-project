from typing import List

class Node:
    #node contains name(string), skills(list of strings), difficulty(double)
    def __init__(self, key: int = None, name: str = None, skills: List[str] = None, difficulty: float = None, probability: float = None) -> None:
        self.name = name
        self.skills = skills
        self.difficulty = difficulty
        self.key = key

    # def __init__(self, key) -> None:
    #     self.key = key

    def __repr__(self):
        return f"Node({self.key})"