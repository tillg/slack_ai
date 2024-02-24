from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging
import json
import inspect
from dotenv import load_dotenv
from utils import get_logger
from openai import OpenAI
from pprint import pprint, pformat
from chatgpt import ChatGPT


load_dotenv()

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_BASE_URL = os.environ['OPENAI_BASE_URL']

chat_gpt = ChatGPT(completion_hparams={"api_key": OPENAI_API_KEY, "base_url": OPENAI_BASE_URL})
chat_gpt.system("You are a poetic assistant, skilled in explaining everything with creative flair.")

app = App(token=SLACK_BOT_TOKEN)
# client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

#@app.event("app_mention")
@app.event("message")
def message_handler(body, say):
    logger = get_logger("message_handler", logging.INFO)
    formatted_body = pformat(body)
    logger.info(f"Body: {formatted_body}")

    question = body["event"]["text"]
    logger.info(f"question: {question}")

    answer = "I'm sorry, I'm not able to answer that question at the moment."
    try:
        answer = chat_gpt.chat(question)
    except Exception as e:
        logger.error(f"Error: {e}")
    logger.info(f"Answer: {answer}")
    say(answer)
    return

@app.event("message")
def message_handler(body, say):
    logger = get_logger("message_handler", logging.INFO)
    formatted_body = pformat(body)
    logger.info(f"Body: {formatted_body}")
    return 

def add_message_to_message_stack(message_stack, role, content):
    message_stack.append(question)
    return message_stack

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


