import random
import subprocess
import ast
import re

import numpy as np

def genQuestion(topic : str):
    
        result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')

        #ai start
        cleaned_lines = result.splitlines()
        try:
            
            error_message = "AttributeError: `itemset` was removed from the ndarray class in NumPy 2.0. Use `arr[index] = value` instead."
            error_index = next(i for i, line in enumerate(cleaned_lines) if error_message in line)
            cleaned_lines = cleaned_lines[error_index + 1:]
        except:
            pass
        #ai end

        print(result)
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

def genQuestion2(topic : str):
    result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')

    print(result)
    qa_pairs = ast.literal_eval(result)
    pair = qa_pairs[0]
    question = pair[0].strip()
    answer = pair[1].strip()
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")

    options = changeItUp(answer)
    options.append(answer)
    random.shuffle(options)
    #ans = int(answer)
    
    for i in options:
           print(i)
    
    return [question, answer, options]

#print(changeItUp("[4,-9.7]"))
genQuestion2('polynomial_roots')

