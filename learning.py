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
    
    def changeItUp(expr : str):
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
        result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')

        print(result)
        qa_pairs = ast.literal_eval(result)
        pair = qa_pairs[0]
        question = pair[0].strip()
        answer = pair[1].strip()
        
        print(f"Question: {question}")
        print(f"Answer: {answer}")

        options = self.changeItUp(answer)
        options.append(answer)
        random.shuffle(options)
        #ans = int(answer)
        
        for i in options:
            print(i)
        
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


