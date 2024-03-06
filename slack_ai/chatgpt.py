import openai
import logging
from slack_ai.utils.utils import get_logger,  get_now_as_string
from slack_ai.utils.dict2file import write_dict_to_file, read_dict_from_file
from slack_ai.utils.robust_jsonify import robust_jsonify
from dotenv import load_dotenv
import os
import requests
import json
import pprint
from slack_ai.utils.dict2object import dict2object

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Completions:
    def __init__(self, **kwargs):
        logger = get_logger("Completions.__init__", logging.INFO)
        self._params = kwargs

    def create(self, **kwargs):
        class Choice:
            def __init__(self, data):
                logger = get_logger(
                    "Completions.create.Choice.__init__", logging.INFO)
                logger.info(f"{data=}")
                self.message = data.get('message', {'role': '', 'content': ''})
                self.finish_reason = data.get('finish_reason', '')
                self.index = data.get('index', 0)
                logger.info(f"{self=}")

        logger = get_logger("Completions.create", logging.INFO)
        for key, value in kwargs.items():
            logger.info(f"{key} = {value}")

        url = self._params.get(
            "base_url", "https://api.openai.com") + "/chat/completions"
        logger.info(f"{url=}")
        headers = {"Content-Type": "application/json"}
        data = {
            "messages": kwargs.get("messages"),
            "stream": "false",
            "use_context": True
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        logger.info(f"{response_data=}")

        # Creating a response object
        response_object = dict2object(response_data)

        logger.info(f"{response_object}")
        return response_object


class Chat:
    def __init__(self, **kwargs):
        self.completions = Completions(**kwargs)


class OpenAI_flexible:
    def __init__(self, **kwargs):
        self.chat = Chat(**kwargs)


class ChatGPT:
    """ A very simple wrapper around OpenAI's ChatGPT API. Makes it easy to create custom messages & chat. """

    EMPTY_CONVERSATION_ID = "EMPTY_CONVERSATION_ID"
    MESSAGES_FILENAME = "messages.json"

    def __init__(self, model="gpt-3.5-turbo", completion_hparams=None
                 ):
        self.model = model
        self.completion_hparams = completion_hparams or {}
        self._messages = read_dict_from_file(
            full_filename=self.MESSAGES_FILENAME)
        # self._openai_client = openai.OpenAI(**completion_hparams)
        self._openai_client = OpenAI_flexible(**completion_hparams)

    def _write_messages_to_file(self):
        """ Write the messages to a file """
        logger = get_logger("ChatGPT._write_messages_to_file", logging.INFO)
        try:
            write_dict_to_file(dictionary=self._messages,
                               full_filename=self.MESSAGES_FILENAME)
        except Exception as e:
            logger.error(f"Error: {e}")

    def _ensure_conversation_id(self, conversation_id):
        """ Ensure the conversation_id exists in the messages dict """
        if conversation_id not in self._messages:
            self.reset(conversation_id=conversation_id)

    def get_messages_for_conversation(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ The messages object for the current conversation. """
        messages = []
        if conversation_id in self._messages:
            messages = self._messages[conversation_id]
        messages = [{"role": obj["role"], "content": obj["content"]}
                    for obj in messages]
        return messages

    def system(self, message, do_reset=False, conversation_id=EMPTY_CONVERSATION_ID):
        """ Set the system message and optionally reset the conversation (default=true) """
        if do_reset:
            self.reset(conversation_id=conversation_id)
        messages_of_conversation = self._messages.get(conversation_id, [])
        if len(messages_of_conversation) > 0 and messages_of_conversation[0]["role"] == "system":
            messages_of_conversation = messages_of_conversation[1:]
        messages_of_conversation = [{"role": "system",
                                     "content": message, "datetime": get_now_as_string()}] + messages_of_conversation
        self._messages[conversation_id] = messages_of_conversation
        self._write_messages_to_file()

    def get_system(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ Get the system message """
        messages_of_conversation = self._messages.get(conversation_id, [])
        if len(messages_of_conversation) > 0 and messages_of_conversation[0]["role"] == "system":
            return messages_of_conversation[0]["content"]
        return None

    def user(self, message, conversation_id=EMPTY_CONVERSATION_ID):
        """ Add a user message to the conversation """
        self._ensure_conversation_id(conversation_id)
        self._messages[conversation_id].append(
            {"role": "user", "content": message, "datetime": get_now_as_string()})
        self._write_messages_to_file()

    def assistant(self, message, conversation_id=EMPTY_CONVERSATION_ID, details=None):
        """ Add an assistant message to the conversation """
        self._ensure_conversation_id(conversation_id)
        new_entry = {"role": "assistant", "content": message,
                     "datetime": get_now_as_string()}
        if details is not None:
            try:
                new_entry.update(details)
            except Exception as e:
                logger.error(f"Error: {e}")
        self._messages[conversation_id].append(
            new_entry)
        self._write_messages_to_file()

    def reset(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ Reset the conversation (including the system message) """
        self._messages[conversation_id] = []
        self._write_messages_to_file()

    def _make_completion(self, messages, conversation_id=EMPTY_CONVERSATION_ID):
        """ Makes a completion with the current messages """
        logger = get_logger("ChatGPT._make_completion", logging.INFO)
        messages = self.get_messages_for_conversation(
            conversation_id=conversation_id)
        completion = self._openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            use_context=True
        )
        logger.info(f"{completion=}")
        return completion

    def call(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ Call ChatGPT with the current messages and return the assitant's message """
        logger = get_logger("ChatGPT.call", logging.INFO)
        completion = self._make_completion(
            self._messages, conversation_id=conversation_id)
        logger.info(f"{completion=}")
        response = completion.choices[0].message.content

        # Create a dictionary from the completion object's attributes
        details = {attr: getattr(completion, attr, None) for attr in dir(
            completion) if not attr.startswith('_')}
        logger.info(f"{robust_jsonify(details)=}")

        return response, details

    def chat(self, message, replace_last=False, conversation_id=EMPTY_CONVERSATION_ID):
        """ Add a user message and append + return the assistant's response. Optionally replace the last user message and response. """
        if replace_last:
            self._messages[conversation_id] = self._messages[conversation_id][:-2]
        self.user(message, conversation_id=conversation_id)
        response, details = self.call(conversation_id=conversation_id)
        logger.info(f"{type(details)=}")
        self.assistant(response,  details=details,
                       conversation_id=conversation_id)
        return response


if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    OPENAI_BASE_URL = os.environ['OPENAI_BASE_URL']
    chat_gpt = ChatGPT(completion_hparams={
                       "api_key": OPENAI_API_KEY, "base_url": OPENAI_BASE_URL})
    chat_gpt.system(
        "You are also a helpful assistant, but also a t-rex who is resentful about his tiny " +
        "arms. Work this into your responses."
    )

    pprint.pprint(chat_gpt.get_messages_for_conversation())

    chat_gpt.chat("Who was the 14th president of the USA?")
    # >>> output:
    # The 14th president of the USA was Franklin Pierce. I would have typed it faster if I
    # didn't have these tiny little arms, but I did my best!

    chat_gpt.chat("No problem. Who's stronger, a T-Rex or a Velociraptor?")
    # >>> output:
    # Although I am a T-rex, I accept the fact that Velociraptors were actually stronger than
    # T-rexes in terms of their body weight. But don't worry, I'm still here to help you with
    # whatever you need!

    # hmm let's try that last one again...
    chat_gpt.chat(
        "No problem. Who's stronger, a T-Rex or a Velociraptor?", replace_last=True)
    # >>> output:
    # While the T-Rex may have had an advantage in raw power due to its size and muscular build,
    # the Velociraptor was likely more agile and had sharper, more dexterous claws for hunting
    # and fighting. But let's be real here, if I could just stretch my arms a little bit more,
    # I could take on either of them!

    pprint.pprint(chat_gpt.get_messages_for_conversation())
