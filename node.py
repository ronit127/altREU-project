from typing import List

class Question: 
    def __init__(self, prompt: str, options: List[str], answer: str) -> None:
        self.prompt = prompt
        self.options = options
        self.answer = answer
        
class Node:
    #node contains name(string), skills(list of strings), difficulty(double)
    def __init__(self, key: int = None, name: str = None, topic: str = None, difficulty: float = None, question: Question = None) -> None:
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.key = key
        self.question = question

    # def __init__(self, key) -> None:
    #     self.key = key

    def __repr__(self):
        return f"Node({self.key})"