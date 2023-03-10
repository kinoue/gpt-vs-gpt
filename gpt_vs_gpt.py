import time
import datetime
import base64
import streamlit as st
from streamlit_chat import message
from collections import OrderedDict
from openai_client import ask_opinion

st.header("GPT vs GPT")
st.write('''
    Ask GPT to discuss any topics. You specifiy the topic of the discussion, and
    GPT will generate a discussion between the two opposing views on the topic.
''')

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

def ask_gpt():
    # autoplay_audio("the_voice.wav")
    if not topic:
        st.error("Please provide the topic first.")
    else:
        statements = st.session_state.statements
        print(f'Current statements length: {len(statements)}')

        for turn in range(num_turns):
            if len(statements) == 0:
                statements.append(ask_opinion(topic, stance))
                statements.append(ask_opinion(topic, stance, statements[-1]))
            else:
                statements.append(ask_opinion(topic, stance, statements[-1], statements[-2]))
                statements.append(ask_opinion(topic, stance, statements[-1], statements[-2]))
            print(f'Current statements length: {len(statements)}')
            print(f'last statement: {statements[-1]}')

# autoplay_audio(verition.create_and_download_voice("the_voice", "oh yes! i'm here!!"))

with control_area.container():
    topic = st.text_input(
        label='Topic (e.g. "birth control", "the best basketball player in the history", "who is the strongest Avenger?"):',
        key="topic"
    )
    num_turns = st.select_slider(
        label='Number of Turns: ',
        options=[1, 2, 3, 4, 5],
        value=2
    )
    stance = st.select_slider(
        label='Stance: ',
        options=["Moderate", "Constructive", "Radical"],
        value="Constructive"
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