import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.assistant_v2 import MessageInputStateless, MessageInputOptions
from environment import assistant_key, assistant_url, assistant_id


def setup_assistant():
    authenticator = IAMAuthenticator(assistant_key)
    assistant = AssistantV2(
        version='2021-11-27',
        authenticator=authenticator
    )
    assistant.set_service_url(assistant_url)
    return assistant


def send_stateless_message(text):
    assistant = setup_assistant()

    response = assistant.message_stateless(
        assistant_id=assistant_id,
        input=MessageInputStateless(text=text)
    ).get_result()
    watson_text_response = response["output"]["generic"][0]["text"]
    return watson_text_response


def new_session():
    assistant = setup_assistant()

    response = assistant.create_session(
        assistant_id=assistant_id
    ).get_result()
    print(response["session_id"])
    return response["session_id"]


def message(session_id, text):
    assistant = setup_assistant()

    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input= {
            'message_type': 'text',
            'text': text,
            'options': {'return_context': True}
        }
    ).get_result()


    return (response["output"]["generic"][0]["text"], get_context_variables_from_response(response))


def get_context_variables_from_response(response):
    try:
        context_variables = response["context"]["skills"]["main skill"]["user_defined"]
        print("context variables: ", context_variables, "\n")
    except (TypeError, KeyError):
        return False

    if context_variables.get('activity') == 'language':
        required_variables = {'activity', 'language', 'difficulty'}

    elif context_variables.get('activity') == 'music':
        required_variables = {'activity', 'language'}

    else:
        required_variables = {'activity', 'language'}

    if required_variables.issubset(set(context_variables)):
        context_variables = {k: v.lower() for k, v in context_variables.items()}

        return context_variables
    else:
        return False
