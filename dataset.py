import random
import subprocess

def genQuestion(topic : str):
    
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

genQuestion("linear_1d")