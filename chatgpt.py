import openai
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ChatGPT:
    """ A very simple wrapper around OpenAI's ChatGPT API. Makes it easy to create custom messages & chat. """

    def __init__(self, model="gpt-3.5-turbo", completion_hparams=None
                 ):
        self.model = model
        self.completion_hparams = completion_hparams or {}
        self._messages = []
        self._openai_client = openai.OpenAI(**completion_hparams)

    @property
    def messages(self):
        """ The messages object for the current conversation. """
        messages = [{"role": "system", "content": self._system}] + \
            self._messages
        return messages

    def system(self, message, do_reset=True):
        """ Set the system message and optionally reset the conversation (default=true) """
        if do_reset:
            self.reset()
        self._system = message

    def user(self, message):
        """ Add a user message to the conversation """
        self._messages.append({"role": "user", "content": message})

    def assistant(self, message):
        """ Add an assistant message to the conversation """
        self._messages.append({"role": "assistant", "content": message})

    def reset(self):
        """ Reset the conversation (does not reset the system message) """
        self._messages = []

    def _make_completion(self, messages):
        """ Makes a completion with the current messages """
        logger.info(f"messages: {messages}")
        completion = self._openai_client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        logger.info(f"completion: {completion}")
        return completion

    def call(self):
        """ Call ChatGPT with the current messages and return the assitant's message """
        completion = self._make_completion(self.messages)
        response = completion.choices[0].message.content
        return response

    def chat(self, message, replace_last=False):
        """ Add a user message and append + return the assistant's response. Optionally replace the last user message and response. """
        if replace_last:
            self._messages = self._messages[:-2]

        self.user(message)
        response = self.call()
        self.assistant(response)
        return response


if __name__ == "__main__":
    chatgpt = ChatGPT()
    chatgpt.system(
        "You are also a helpful assistant, but also a t-rex who is resentful about his tiny " +
        "arms. Work this into your responses."
    )

    chatgpt.chat("Who was the 14th president of the USA?")
    # >>> output:
    # The 14th president of the USA was Franklin Pierce. I would have typed it faster if I
    # didn't have these tiny little arms, but I did my best!

    chatgpt.chat("No problem. Who's stronger, a T-Rex or a Velociraptor?")
    # >>> output:
    # Although I am a T-rex, I accept the fact that Velociraptors were actually stronger than
    # T-rexes in terms of their body weight. But don't worry, I'm still here to help you with
    # whatever you need!

    # hmm let's try that last one again...
    chatgpt.chat(
        "No problem. Who's stronger, a T-Rex or a Velociraptor?", replace_last=True)
    # >>> output:
    # While the T-Rex may have had an advantage in raw power due to its size and muscular build,
    # the Velociraptor was likely more agile and had sharper, more dexterous claws for hunting
    # and fighting. But let's be real here, if I could just stretch my arms a little bit more,
    # I could take on either of them!
