import os
import openai
import logging

logging.basicConfig(filename='gpt-vs-gpt.log', encoding='utf-8', level=logging.DEBUG)

openai.api_key = os.environ["OPENAI_API_KEY"]

## Extra parameters if you are using Azure
openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

def ask_opinion(topic, stance, temperature, opposing_opinion=None, previous_opinion=None):
    if previous_opinion is None:
        if opposing_opinion is None:
            return ask_opinion_first(topic, stance, temperature)
        else:
            return ask_opinion_againt(topic, stance, temperature, opposing_opinion)
    return ask_opinion_followup(topic, stance, temperature, opposing_opinion, previous_opinion)

def ask_opinion_first(topic, stance, temperature):
    prompt = f'''
        State your position on the issue of {topic} briefly.
        Be opinionated and be {stance}. Don't be ambigous.
        Ask the opponent's opinion.
    '''
    max_tokens=(200 + int(len(prompt.split(' ')) * 1.5))
    response = openai.Completion.create(
        engine="text-davinci-003", # engine is a pramereter for Azure. It should be model if OpenAI 
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    opinion = response['choices'][0]['text'].strip()
    logging.info(f"prompt:     {prompt}")
    logging.info(f"max_tokens: {max_tokens}")
    logging.info(f"response:   {opinion}")
    return opinion

def ask_opinion_againt(topic, stance, temperature, opposing_opinion):
    prompt = f'''
        State your position on the issue of {topic} briefly.
        Be opinionated and be {stance}.
        Take the oppositve view of the following opinion: {opposing_opinion}.
    '''
    max_tokens=(200 + int(len(prompt.split(' ')) * 1.5))
    response = openai.Completion.create(
        engine="text-davinci-003", # engine is a pramereter for Azure. It should be model if OpenAI
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    opinion = response['choices'][0]['text'].strip()
    logging.info(f"prompt:     {prompt}")
    logging.info(f"max_tokens: {max_tokens}")
    logging.info(f"response:   {opinion}")
    return opinion


def ask_opinion_followup(topic, stance, temperature, opposing_opinion, previous_opinion):
    prompt = f'''
        State your position on the issue of {topic} briefly.
        Be opinionated and be {stance}. Don't be ambigous.
        Build on top of the previous statmement: {previous_opinion}.
        Argue against the following opposing opinion: {opposing_opinion}.
    '''
    max_tokens=(200 + int(len(prompt.split(' ')) * 1.5))
    response = openai.Completion.create(
        engine="text-davinci-003", # engine is a pramereter for Azure. It should be model if OpenAI
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    opinion = response['choices'][0]['text'].strip()
    logging.info(f"prompt:     {prompt}")
    logging.info(f"max_tokens: {max_tokens}")
    logging.info(f"response:   {opinion}")
    return opinion
