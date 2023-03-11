import sys
import json
import streamlit as st
from streamlit_chat import message

sys.path.append('../')
from db_helper import get_dialogues
from db_helper import get_statements
from db_helper import increment_dialogue_view

st.header('History')

dialogues = get_dialogues()

control_area = st.empty()
dialogue_area = st.empty()
download_area = st.empty()

with control_area.container():

    if dialogues and len(dialogues) > 0:
        table_text = ""
        table_text += "| Topic | Stance | Temperature | Turns | Views | |\n"
        table_text += "|:------|:-------|:------------|:------|-------|-|\n"

        for d in dialogues.values():
            table_text += "| {} | {} | {} | {} | {} | [Open](history?dialogue_id={}) |\n".format(
                d['topic'], d['stance'], d['temperature'], d['num_turns'], d['views'], d['id']
            )
        print(table_text)
        st.write(table_text)


with dialogue_area.container():
    _params = st.experimental_get_query_params()

    if _params.get('dialogue_id'):
        _dialogue_id = int(_params['dialogue_id'][0])
        _dialogue = dialogues[_dialogue_id]
        increment_dialogue_view(_dialogue_id)
        st.text('')
        st.write(f'''
            |                  |                           |
            |:-----------------|:--------------------------|
            | Topic:           | {_dialogue['topic']}      |
            | Stance:          | {_dialogue['stance']}     |
            | Temperature:     | {_dialogue['temperature']}|
            | Number of Turns: | {_dialogue['num_turns'] } |
        ''')
        st.text('')
        _statements = get_statements(_dialogue_id).values()
        if _statements:
            for _i, _statement in enumerate(_statements):
                print(f"{_i}: {_statement}")
                message(
                    _statement['statement'],
                    is_user=(_i % 2 == 1),
                    key=str(_i) + '_user',
                    avatar_style='bottts',
                    seed=(_i % 2)
                )

with download_area.container():
    st.write("")
    st.write("")
    col1, col2 = st.columns(2)
    with col1.container():
        st.download_button(
            label="Download Dialogue Data",
            data=json.dumps(list(dialogues.values()), indent=4),
            file_name='dalogues.json',
            mime='application/json',
        )

    with col2.container():
        st.download_button(
            label="Download Statement Data",
            data=json.dumps(list(get_statements().values()), indent=4),
            file_name='dalogues.json',
            mime='application/json',
        )

