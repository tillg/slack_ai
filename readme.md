# slack_ai

My local AI system accessible via Slack.

![Overview](overview.svg)

See what it looks like:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=8y4jwXNwdSU" target="_blank">
 <img src="http://img.youtube.com/vi/8y4jwXNwdSU/hqdefault.jpg" alt="Watch the video" width="400" border="5" />
</a>

Click on the picture to see the video.

## Features & known problems

* Talk to your local LLM via Slack
* Each slack channel corresponds to a conversation.
* All the conversations as well as the system prompts are tracked in a human readable JSON file. Conversations are re-loaded from this file at Bot startup.
* Use slack commends:
  * `/system` Shows & sets the system prompt for the current channel.

**⚠️ Beware**
* The system is neither multi-user capable nor meant to deal with a lot of load. The conversations are read & written to a local JSON file in an *optimistic* way.
## Getting things going

* Get a local LLM running that offers access via an [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create). I used [LM Studio on my Mac](https://lmstudio.ai).
* Clone this repo 
* Make sure u have python 3.12 or so
* `pip install -r requirements.txt`
* Create a `.env` file and edit it: `cp sample.env .env`
* Start the thing with `python app.py` and watch the logs scroll 😉

# To Do

* Describe in the readme how to set up the bot in Slack

## Reading / Problems / Solutions

* [Slack Bolt Framework - Listening to events](https://slack.dev/bolt-python/concepts#event-listening)
* [How to Build a Slackbot with Python](https://www.kubiya.ai/resource-post/how-to-build-a-slackbot-with-python)
* Took this [ChatGPT class](https://gist.github.com/joeddav/a11e5cc0850f0e540324177a53b547ae)



