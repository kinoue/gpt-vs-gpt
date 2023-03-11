import time
import json
import datetime
import base64
import streamlit as st
import sqlite3 as sl
from streamlit_chat import message
from openai_client import ask_opinion
from db_helper import add_dialogue

st.header("GPT vs GPT")
st.write('''
    Ask GPT to discuss any topics. You specifiy the topic of the discussion, and
    GPT will generate a discussion between the two opposing views on the topic.
''')
st.sidebar.success("Select a page above")

if 'statements' not in st.session_state:
    st.session_state['statements'] = []

control_area = st.empty()
dialogue_area = st.empty()

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def add_to_history(statements):
    history = json.load(open('history.json', 'r'))
    history.append(
        {
            'topic': topic,
            'stance': stance,
            'num_turns': num_turns,
            'statements': statements
        }
    )
    json.dump(history, open('history.json', 'w'))

def ask_gpt():
    if not topic:
        st.error("Please provide the topic first.")
    else:
        _statements = st.session_state.statements
        for turn in range(num_turns):
            if len(_statements) == 0:
                _statements.append(ask_opinion(topic, stance))
                _statements.append(ask_opinion(topic, stance, _statements[-1]))
            else:
                _statements.append(ask_opinion(topic, stance, _statements[-1], _statements[-2]))
                _statements.append(ask_opinion(topic, stance, _statements[-1], _statements[-2]))

    history = json.load(open('history.json', 'r'))
    history.append(
        {
            'topic': topic,
            'stance': stance,
            'num_turns': num_turns,
            'temperature': temperature,
            'statements': _statements
        }
    )
    json.dump(history, open('history.json', 'w'))


with control_area.container():
    topic = st.text_input(
        label='Topic (e.g. "birth control", "the best basketball player in the history", "who is the strongest Avenger?"):',
        key="topic"
    )
    stance = st.select_slider(
        label='Stance: ',
        options=["Moderate", "Constructive", "Radical"],
        value="Constructive"
    )
    num_turns = st.select_slider(
        label='Number of Turns: ',
        options=[1, 2, 3, 4, 5],
        value=3
    )
    temperature = st.select_slider(
        label='Temperature: ',
        options=range(0.0, 1.1, 0.1),
        value=0.5
    )
    st.button("Ask GPT", on_click=ask_gpt)

with dialogue_area.container():
    if st.session_state.statements:
        for i, statement in enumerate(st.session_state.statements):
            print(f"{i}: {statement}")
            message(
                statement,
                is_user=(i % 2 == 1),
                key=str(i) + '_user',
                avatar_style='bottts',
                seed=(i % 2)
            )