import json
import streamlit as st
from streamlit_chat import message

st.header('History')
st.title('History')

control_area = st.empty()
dialogue_area = st.empty()

def display_dialogue(dialogue):
    if not topic:
        st.error("Please provide the topic first.")
    if not history:
        st.error("History not found. 😢")
    else:
        statements = st.session_state.statements
        for turn in range(num_turns):
            if len(statements) == 0:
                statements.append(ask_opinion(topic, stance))
                statements.append(ask_opinion(topic, stance, statements[-1]))
            else:
                statements.append(ask_opinion(topic, stance, statements[-1], statements[-2]))
                statements.append(ask_opinion(topic, stance, statements[-1], statements[-2]))

history = json.load(open('history.json'))

for h in history:
    history_dict = 
history = sorted(history, key=lambda h: h['topic'] + h['stance'] + str(h['num_turns']))

with control_area.container():
    st.download_button(
        label="Download History as JSON",
        data=open('history.json'),
        file_name='history.json',
        mime='application/json',
    )

    selection = st.selectbox(
        'Select Topic',
        options=history,
        on_change=display_dialogue,
        format_func = lambda h: f"{h['topic']} ({h['stance']}, {h['turns']} turns)"
    )

with dialogue_area.container():
    if selection:
        for dialogue in history:
            if dialogue['topic'] == 
