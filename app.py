import streamlit as st
import time
import numpy as np 
import matplotlib.pyplot as plt 
from node import Node, Question
from graph import Graph
from learning import ExpertGraph

# questions = [
#     {   
#         "key": 0,
#         "question": "What is the capital of France?",
#         "options": ["Berlin", "London", "Paris", "Madrid"],
#         "answer": "Paris",
#         "skills": ["expressions", "linear equations"]
#     },
#     {   
#         "key": 1,
#         "question": "What is 2 + 2?",
#         "options": ["3", "4", "5", "6"],
#         "answer": "4",
#         "skills": ["expressions", "quadratic equations"]
#     },
#     {   
#         "key": 2,
#         "question": "What is the largest planet in our solar system?",
#         "options": ["Earth", "Mars", "Jupiter", "Saturn"],
#         "answer": "Jupiter",
#         "skills": ["inequalities"]
#     }
# ]

# question_list = [Node(key = q["key"], skills = q["skills"], question = Question(q["question"], q["options"], q["answer"])) for q in questions] # AI-assisted line

# if 'expert' not in st.session_state:
#     graph = Graph({})
#     graph.createEdge(question_list[0], question_list[1], -1.0)
#     graph.createEdge(question_list[1], question_list[2], -1.0)  
#     st.session_state.expert = ExpertGraph(graph)

# if 'score' not in st.session_state:
#     st.session_state.score = 0

# if 'current_question' not in st.session_state:
#     st.session_state.current_question = st.session_state.expert.nextQuestion()

# def display_question(question: Question):
#     st.write(question.prompt)
#     user_answer = st.radio("Choose an answer:", question.options)
#     return user_answer

# def check_answer(user_answer, correct_answer, skills):
#     if user_answer == correct_answer:
#         st.success("Correct!")
#         st.session_state.expert.updateSkills(skills, True)
#         st.session_state.score += 1
#     else:
#         st.error(f"Wrong! The correct answer is {correct_answer}.")
#         st.session_state.expert.updateSkills(skills, False)

# st.title("Personalized Learning App")

# reminder = st.write("(Make sure to update how you feel whilst answering the questions. Good luck!)")

# st.write()
# st.write()
# st.write()

# if 'motivation' not in st.session_state:
#     st.session_state.motivation = 0.5

# if 'comfort' not in st.session_state:
#     st.session_state.comfort = 0.5

# def update_point(x, y): 
#     st.session_state.expert.motivation = x
#     st.session_state.expert.comfort = y
#     st.session_state.motivation = x 
#     st.session_state.comfort = y 


# if st.session_state.current_question is not None:
#     current_q = st.session_state.current_question
#     user_answer = display_question(current_q.question)

#     if st.button("Submit"):

#         check_answer(user_answer, current_q.question.answer, current_q.skills)
#         if st.session_state.expert.availableQuestions():
#             st.session_state.current_question = st.session_state.expert.nextQuestion()
#         else:
#             st.session_state.current_question = None

#         time.sleep(2)
#         st.rerun()
# else:
#     st.write(f"Quiz completed! Your score is {st.session_state.score}/{len(questions)}.")


# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")

# motivation = st.slider("Rate your motivation (0 - 1)", 0.0, 1.0, st.session_state.motivation) 
# comfort = st.slider("Rate your comfort (0 - 1)", 0.0, 1.0, st.session_state.comfort) 
# update_point(motivation, comfort) 

# fig, ax = plt.subplots() 
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1) 
# ax.set_xlabel('User Comfort') 
# ax.set_ylabel('User Motivation') 
# ax.grid() 
# ax.plot(st.session_state.motivation, st.session_state.comfort, 'ro') 

# st.pyplot(fig) 










# st.title('Systems of Equations')

# st.subheader('Question 14:')
# question_type = "Solve the following equation"

# question = question_type +":  \n" + "x + 4y = 8   \n 2x - y = -2"
# options = ["A. (2,1)", "B. (1,2)", "C. (2,0)", "D. (0,2)", "E. No Solution"]

# correct_option = "D. (0,2)"

# st.write(question)


# # Input field for user's answer
# user_answer = st.radio('Choose your answer:', options)

# if st.button('Submit'):
#     if user_answer == correct_option:
#         st.success('Correct!')
#     else:
#         error_text = "Incorrect. The correct answer is " + correct_option
#         st.error(error_text)

# st.button('Next Question')

# st.markdown("&nbsp;" * 350)

# 

# if 'x' not in st.session_state: 
#     st.session_state.x = 0.5 
# if 'y' not in st.session_state: 
#     st.session_state.y = 0.5 


