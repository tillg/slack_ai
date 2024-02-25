import openai
import logging
from dotenv import load_dotenv
import os
import pprint
from utils import write_dict_to_file, read_dict_from_file, get_now_as_string

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        self._openai_client = openai.OpenAI(**completion_hparams)

    def _write_messages_to_file(self):
        """ Write the messages to a file """
        write_dict_to_file(dictionary=self._messages,
                           full_filename=self.MESSAGES_FILENAME)

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
            new_entry.update(details)
        self._messages[conversation_id].append(
            new_entry)
        self._write_messages_to_file()

    def reset(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ Reset the conversation (including the system message) """
        self._messages[conversation_id] = []
        self._write_messages_to_file()

    def _make_completion(self, messages, conversation_id=EMPTY_CONVERSATION_ID):
        """ Makes a completion with the current messages """
        messages = self.get_messages_for_conversation(
            conversation_id=conversation_id)
        completion = self._openai_client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion

    def call(self, conversation_id=EMPTY_CONVERSATION_ID):
        """ Call ChatGPT with the current messages and return the assitant's message """
        completion = self._make_completion(
            self._messages, conversation_id=conversation_id)
        response = completion.choices[0].message.content
        details = {"model": completion.model, "completion_tokens": completion.usage.completion_tokens,
                   "prompt_tokens": completion.usage.prompt_tokens, "total_tokens": completion.usage.total_tokens}
        model = completion.model
        usage = completion.usage
        return response, details

    def chat(self, message, replace_last=False, conversation_id=EMPTY_CONVERSATION_ID):
        """ Add a user message and append + return the assistant's response. Optionally replace the last user message and response. """
        if replace_last:
            self._messages[conversation_id] = self._messages[conversation_id][:-2]
        self.user(message, conversation_id=conversation_id)
        response, details = self.call(conversation_id=conversation_id)
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
