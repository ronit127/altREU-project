import ast
import re
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
       self.topics_prob : Dict[str, Tuple[float,float]] = {} # maps a skill to a pair of input/output of a sigmoid graph
       # TODO: generate the graph
       self.loadTopics()
       self.motivation = 0.5
       self.comfort = 0.5
       self.questions_complete = 0

    def loadTopics(self, value = 0.25):
        """Loads a baseline probability of 0.25 for all the topics once the graph has been constructed"""
        for node, edges in self.graph.vertexList.items():
            if node.topic in self.topics_prob:
                self.topics_prob[node.topic] = [0,0.25]

    
    def updateTopic(self, topic : str, isCorrect):
            """Updates the estimated probability of the topic of the question answered depending on whether it is correct or not"""
            if topic in self.topics_prob:
                if isCorrect: self.topics_prob[topic][0] += 0.2
                else: self.topics_prob[topic][0] -= 0.2
                self.topics_prob[topic][1] = self.sigmoid(self.topics_prob[topic][0])
    
    def sigmoid(self, x) -> float:
        return 1 / (1+ math.exp(-(x-1.09861)))  
    
    def computeNodeProb(self, node : Node) -> float:
        return self.topics_prob[node.topic].second
    
    def changeItUp(expr : str):
        """Generates similar variants of an expression by changing the numbers in the expression. Accounts for double negatives, and avoids 0's"""
        nums = re.findall(r'-?\d+',expr)
        #print(nums)
        lis = []
        for num in nums:
            lis.append(random.sample([-5,-4,-3,-2,-1,1,2,3,4,5], 3))
        
        new_nums = []
        
        for i in range(len(nums)):
            new_nums.append([])
            for l in lis[i]:
                to_add = int(nums[i]) + l
                if to_add == 0: 
                    new_nums[i].append(2)  
                else:
                    new_nums[i].append(to_add)
        #print(new_nums)
        new_expr = [expr for i in range(3)]
        for j in range(3):
            for i in range(len(nums)):
                # print(new_nums[i][j])
                # print("im replacing " + nums[i] + " with " + str(new_nums[i][j]))
                new_expr[j] = re.sub(r'(?<!\d){}(?!\d)'.format(re.escape(nums[i])), str(new_nums[i][j]), new_expr[j], 1)
                #new_expr[j] = new_expr[j].replace(nums[i], str(new_nums[i][j]), 1)]
                new_expr[j] = new_expr[j].replace(" - -", " + ")

        return new_expr

    def genQuestion(self, topic : str):  
        """Generates a question of a given topic returning a Question object"""

        result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')

        print(result)
        qa_pairs = ast.literal_eval(result)
        pair = qa_pairs[0]
        question = pair[0].strip()
        answer = pair[1].strip()
        
        #print(f"Question: {question}")
        #print(f"Answer: {answer}")

        options = self.changeItUp(answer)
        options.append(answer)
        random.shuffle(options)
        #ans = int(answer)
        
        return Question(question, options, answer)
        
    def nextQuestion(self) -> Node:
        randomNode : Node = random.choice(list(self.graph.vertexList.keys()))
        self.questions_complete = self.questions_complete + 1
        return randomNode

    def availableQuestions(self):
        return self.questions_complete < len(self.graph.vertexList.keys())
    
    #function that returns the estimated cost of travelling to the end (should be high if far away in the skill tree)
    def heurestic(node: Node) -> float:
        pass


# curr_node = Node()


