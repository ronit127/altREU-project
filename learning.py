from graph import Graph 
from node import Node, Question
from typing import Dict,Tuple,List
import numpy as np
import random
import math
import subprocess


class ExpertGraph:
    def __init__(self, the_graph : Graph):
       self.graph = the_graph 
       self.skills_prob : Dict[str, Tuple[float,float]] = {} # maps a skill to a pair of input/output of a sigmoid graph
       self.loadSkills()
       self.motivation = 0.5
       self.comfort = 0.5
       self.questions_complete = 0

    def loadSkills(self, value = 0.25):
        for node, edges in self.graph.vertexList.items():
            for skill in node.skills:
                if skill in self.skills_prob:
                    self.skills_prob[skill] = [0,0.25]

    def updateSkills(self, skills : List[str], isCorrect):
        for skill in skills:
            if skill in self.skills_prob:
                if isCorrect: self.skills_prob[skill][0] += 0.2
                else: self.skills_prob[skill][0] -= 0.2
                self.skills_prob[skill][1] = self.sigmoid(self.skills_prob[skill][0])
    
    def sigmoid(self, x) -> float:
        return 1 / (1+ math.exp(-(x-1.09861)))  
    
    def computeNodeProb(self, node : Node) -> float:
        skill_list = []
        for i in node.skills:
            if self.skills_prob.__contains__(i):
                skill_list.append(self.skills_prob[i])
        return np.min(skill_list)
    
    #generates a question given a topic
    def genQuestion(self, topic : str):
        result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')

        #ai start
        cleaned_lines = result.splitlines()
        try:
            
            error_message = "AttributeError: `itemset` was removed from the ndarray class in NumPy 2.0."
            error_index = next(i for i, line in enumerate(cleaned_lines) if error_message in line)
            cleaned_lines = cleaned_lines[error_index + 1:]
        except:
            pass
        #ai end

        #print(result)
        question = cleaned_lines[2]
        answer = int(cleaned_lines[3])
        done = False 
        same = False 
        while (not done):
            opt = random.sample(range(answer - 10, answer + 10), 3) 
            for i in range(0, 3, 1):
                        if (opt[i] == answer):
                                same = True 
                        if (i == 2 and not same):
                                done = True   
            same = False 

        opt.append(answer) 
        options = [str(x) for x in opt]
        random.shuffle(options) 
        print(options)
        print("question: " + question)
        print("answer: " + str(answer))
        return [question, answer, options]
        
    def nextQuestion(self) -> Node:
        randomNode : Node = random.choice(list(self.graph.vertexList.keys()))
        self.questions_complete = self.questions_complete + 1
        return randomNode

    def availableQuestions(self):
        return self.questions_complete < len(self.graph.vertexList.keys())
    
    #function that returns the estimated cost of travelling to the end (should be high if far away in the skill tree)
    def heurestic(node: Node) -> float:
        pass


#  self.skills_prob["linear"] = 0.25
#  self.skills_prob["quadratic"] = 0.29
a_node = Node(1, skills = ["linear", "quadratic"])

# curr_node = Node()


