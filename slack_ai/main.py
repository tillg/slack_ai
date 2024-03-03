from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging
import json
import inspect
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint, pformat
from slack_ai.utils.utils import get_logger
from slack_ai.chatgpt import ChatGPT

load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_BASE_URL = os.environ['OPENAI_BASE_URL']


logger = get_logger("app", logging.INFO)

chat_gpt = ChatGPT(completion_hparams={
                   "api_key": OPENAI_API_KEY, "base_url": OPENAI_BASE_URL})
chat_gpt.system(
    "You are a poetic assistant, skilled in explaining everything with creative flair.")

slack_app = App(token=SLACK_BOT_TOKEN)

class PrettyJson:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return json.dumps(self.data, indent=4, sort_keys=True)

@slack_app.event("message")
def message_handler(body, say):
    logger = get_logger("message_handler", logging.INFO)
    formatted_body = PrettyJson(body)
    logger.info(f"formatted body: {formatted_body}")

    question = body["event"]["text"].strip()
    logger.info(f"{question=}")

    if question == "":
        logger.info("No question, ignoring.")
        return

    channel_id = body["event"]["channel"]
    logger.info(f"{channel_id=}")

    answer = "I'm sorry, I'm not able to answer that question at the moment."
    try:
        answer = chat_gpt.chat(question, conversation_id=channel_id)
    except Exception as e:
        logger.error(f"Error: {e}")
    logger.info(f"Answer: {answer}")
    say(answer)
    return


@slack_app.command("/system")
def system_command(ack, say, body):
    logger = get_logger("system_command", logging.INFO)
    channel_id = body["channel_id"]
    channel_name = body["channel_name"]
    text = body["text"]
    logger.info(f"System command received. {channel_id=}, {channel_name=}, {text=}, {body=}")
    ack()
    system_message = chat_gpt.get_system(
        conversation_id=channel_id) or "No System Prompt set"
    say(f"System prompt for channel {channel_name}: {system_message}")

    if len(text) > 0:
        chat_gpt.system(text, conversation_id=channel_id)
        say(f"System prompt set to: {text}")

    return


@slack_app.event("app_mention")
def handle_app_mention_events(body, logger):
    logger = get_logger("message_handler", logging.INFO)
    formatted_body = pformat(body)
    logger.info(f"{formatted_body=}")
    logger.info("Ignoring event.")
    return


if __name__ == "__main__":
    handler = SocketModeHandler(slack_app, SLACK_APP_TOKEN)
    handler.start()
