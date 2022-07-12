from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from environment import lt_key, lt_url


def setup_lt():
    authenticator = IAMAuthenticator(lt_key)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )

    language_translator.set_service_url(lt_url)

    return language_translator


def translate_language(text, output_langage):
    language_dict = {
        "english": "en",
        "spanish": "es",
        "french": "fr"
    }

    language_translator = setup_lt()
    translation = language_translator.translate(
        text=text,
        target=language_dict[output_langage]).get_result()

    text = translation['translations'][0]['translation']

    return text


print(translate_language("hello, how are you?", "spanish"))