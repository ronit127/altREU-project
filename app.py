import streamlit as st

st.title('Systems of Equations')

st.subheader('Question 14:')
question_type = "Solve the following equation"

question = question_type +":  \n" + "x + 4y = 8   \n 2x - y = -2"
options = ["A. (2,1)", "B. (1,2)", "C. (2,0)", "D. (0,2)", "E. No Solution"]

correct_option = "D. (0,2)"

st.write(question)


# Input field for user's answer
user_answer = st.radio('Choose your answer:', options)

if st.button('Submit'):
    if user_answer == correct_option:
        st.success('Correct!')
    else:
        error_text = "Incorrect. The correct answer is " + correct_option
        st.error(error_text)

st.button('Next Question')

st.markdown("&nbsp;" * 350)

import numpy as np 
import matplotlib.pyplot as plt 

if 'x' not in st.session_state: 
    st.session_state.x = 0.5 
if 'y' not in st.session_state: 
    st.session_state.y = 0.5 

def update_point(x, y): 
    st.session_state.x = x 
    st.session_state.y = y 

x = st.slider("Rate your motivation ( 0 - 1 )", 0.0, 1.0, st.session_state.x) 
y = st.slider("Rate your comfort (0 - 1)", 0.0, 1.0, st.session_state.y) 
update_point(x, y) 

fig, ax = plt.subplots() 
ax.set_xlim(0, 1)
ax.set_ylim(0, 1) 
ax.set_xlabel('User Comfort') 
ax.set_ylabel('User Motivation') 
ax.grid() 
ax.plot(st.session_state.x, st.session_state.y, 'ro') 

st.pyplot(fig) 