from typing import List

class Question: 
    def __init__(self, prompt: str, options: List[str], answer: str) -> None:
        self.prompt = prompt
        self.options = options
        self.answer = answer
        
class Node:
    
    def __init__(self, key, name: str = None, topic: str = None, difficulty: float = None, question: Question = None) -> None:
        '''node contains name(string), skills(list of strings), difficulty(double)'''
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.key = key
        self.question = question

    def __repr__(self):
        return f"Node({self.key})"
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.key == other.key

    def __hash__(self):
        return hash(self.key)