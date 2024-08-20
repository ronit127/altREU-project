import random
import re
import streamlit as st
import time
import numpy as np 
import matplotlib.pyplot as plt 
from node import Node, Question
from graph import Graph
from learning import ExpertGraph

st.title("Personalized Learning App")

if 'hasSubmit' not in st.session_state:
    st.session_state.hasSubmit = False

skill_map = {
    "Addition OR Subtraction": "add_or_sub",
    "Addition AND Subtraction": "add_sub_multiple",
    "Time calculations": "time",
    "Finding a sequence's next term": "sequence_next_term",
    "Finding the nth term of a sequence": "sequence_nth_term",
    "Multiplication": "mul",
    "Division": "div",
    "Multiplication and Division": "mul_div_multiple",
    "Finding the square root": "nearest_integer_root",
    "Solving expressions with square root": "simplify_surd",
    "Combination of all types of arithmetic": "mixed",
    "Unit conversion": "conversion",
    "Solving linear equations": "linear_1d",
    "Solving 2d linear equations": "linear_2d",
    "Finding the roots of polynomials": "polynomial_roots",
    "Finding the first derivative": "differentiate",
    "Finding more advanced derivatives (second, third, etc.)": "differentiate_composed"
}

if 'pre_skills' not in st.session_state:
    st.session_state.pre_skills = []

if 'post_skill' not in st.session_state:
    st.session_state.post_skill = "linear_2d"

if not st.session_state.hasSubmit:
    st.write("What are your previous skills?")

    skills = list(skill_map.keys())
    for skill in skills:
        if st.checkbox(skill):
            st.session_state.pre_skills.append(skill_map[skill])

    st.write(" ")

    chosen_goal = st.radio("What is your goal?", skills)

    if chosen_goal:
        st.session_state.post_skill = skill_map[chosen_goal]

    if st.button("Submit", key="submit_skills"):
        st.session_state.hasSubmit = True
        st.rerun()

if st.session_state.hasSubmit:

    if st.session_state.post_skill in st.session_state.pre_skills: st.session_state.pre_skills.remove(st.session_state.post_skill)

    if 'expert' not in st.session_state:
    
        with st.spinner('Loading Questions...'):
            st.session_state.expert = ExpertGraph(st.session_state.pre_skills, st.session_state.post_skill)
            finished = st.success("Finished!", icon="✅")
            time.sleep(3)
            finished.empty()
            
    if 'score' not in st.session_state:
        st.session_state.score = 0

    if 'current_question' not in st.session_state:
        st.session_state.current_question = st.session_state.expert.nextQuestion()

    col1, col2 = st.columns(2)

    def latex_format(expression: str): 
        #multiplication cases 
        expression = re.sub(r'\*\*(-?\d+)', r'$^{\1}$', expression)  #ai assisted 
        expression = re.sub(r'\*\(', '(', expression)
        expression = re.sub(r'\*([a-zA-Z])', r'\1', expression)
        expression = re.sub(r'(-?\d+)\*(-?\d+)', r'$\1 \\times \2$', expression)
        
        #fraction cases
        expression = re.sub(r'(-?\d+)/(-?\d+)', r'$\\frac{\1}{\2}$', expression)
        expression = re.sub(r'\(([^)]+)\)/\(([^)]+)\)', r'$\\frac{(\1)}{(\2)}$', expression)
        expression = re.sub(r'(\d+)/\(([^)]+)\)', r'$\\frac{\1}{(\2)}$', expression)
        expression = re.sub(r'\(([^)]+)\)/(\d+)', r'$\\frac{(\1)}{\2}$', expression)

        #sqrt case
        expression = re.sub(r'sqrt\(([^)]+)\)', r'$\\sqrt{\1}$', expression)

        return expression

    def display_question(question: Question):
        
        st.write(latex_format(question.prompt))
        choices = []
        for option in question.options:
            choices.append(latex_format(option))  
        user_answer = st.radio("Choose an answer:", choices)
        return user_answer

    def check_answer(user_answer, correct_answer, topic):
        if user_answer == correct_answer:
            st.success("Correct!")
            st.session_state.expert.updateTopic(topic, True)
            st.session_state.score += 1
        else:
            st.error(f"Wrong! The correct answer is {latex_format(correct_answer)}.")
            st.session_state.expert.updateTopic(topic, False)
        st.session_state.expert.updateViability()

    st.write()
    st.write()
    st.write()

    def update_point(x, y): 
        st.session_state.expert.motivation = x
        st.session_state.expert.comfort = y

    if st.session_state.current_question is not None:
        with col1:
            current_q = st.session_state.current_question
            user_answer = display_question(current_q.question)

            if st.button("Submit", key = "submit_ans"):

                check_answer(user_answer, current_q.question.answer, current_q.topic)
                if st.session_state.expert.availableQuestions():
                    st.session_state.current_question = st.session_state.expert.nextQuestion()
                else:
                    st.session_state.current_question = None

                time.sleep(2)
                st.rerun()
    else:
        #st.write(f"Quiz completed! Your score is {st.session_state.score}/{len(questions)}.")
        pass

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    with col2:
        motivation = st.slider("Rate your motivation (0 - 1)", 0.0, 1.0, st.session_state.expert.motivation) 
        comfort = st.slider("Rate your comfort (0 - 1)", 0.0, 1.0, st.session_state.expert.comfort) 
        update_point(motivation, comfort) 

        fig, ax = plt.subplots() 
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1) 
        ax.set_xlabel('User Comfort') 
        ax.set_ylabel('User Motivation') 
        ax.grid() 
        ax.plot(st.session_state.expert.motivation, st.session_state.expert.comfort, 'ro') 

        st.pyplot(fig) 

        st.write("Make sure to update how you feel whilst answering the questions")









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


