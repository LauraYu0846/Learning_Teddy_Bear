import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.assistant_v2 import MessageInputStateless, MessageInputOptions
from environment import assitant_key, assitant_url, assistant_id

def setup_assistant():
    authenticator = IAMAuthenticator(assitant_key)
    assistant = AssistantV2(
        version='2021-11-27',
        authenticator=authenticator
    )
    assistant.set_service_url(assitant_url)
    return assistant



def send_stateless_message(text):
    assistant = setup_assistant()

    # # send message to watson assistant
    response = assistant.message_stateless(
        assistant_id=assistant_id,
        input=MessageInputStateless(text=text)
    ).get_result()
    watson_text_response = response["output"]["generic"][0]["text"]
    print(watson_text_response)

# send_stateless_message("hello")

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
        input={
            'message_type': 'text',
            'text': text,
            'options': {'return_context': True}
        }
    ).get_result()


    return response["output"]["generic"][0]["text"]

    # print(json.dumps(response, indent=2))


def get_context_variables(session_id):
    assistant = setup_assistant()

    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': "",
            'options': {'return_context': True}
        }
    ).get_result()

    return response["context"]["skills"]["main skill"]["user_defined"]



# text = ""
# message("370b9b86-678d-45c0-a585-9c3d8cebe3de", text)


# print(get_context_variables("f3cee332-e684-4333-b07c-900d43be6f2d"))