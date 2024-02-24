# slack_ai

My AI system accessible via Slack.

## Getting things going

* Clone from git
* Make sure u have python 3.12 or so
* `pip -r requirements.txt`
* Create a `.env` file and edit it: `cp sample.env .env`
* Start the thing with `python app.py` and watch the logs scroll 😉

## Log of me doing

### 2024-02-14 Following [How to Build a Slackbot with Python](https://www.kubiya.ai/resource-post/how-to-build-a-slackbot-with-python)

I ran thru the process twice:

1. Building a bot called Till_AI
2. Building a bot called Artificial_Till

#### Create the Slackbot ✅

* Till_AI: Logging into my workspace till_ai
* Artificial_Till: Workspace till_ai

#### Configure the Slackbot ✅

#### Add Scopes ✅

Artificial_Till: Added scopes
* app_mentions:read
* channels:join
* chat:write
* channels:history - maybe that's what I need to read the passed history of the chat

#### Enable Socket Mode ✅

Till_AI Token:
* Name: till_ai_token
* Token: xapp-1-A06LFLB83U3-6708462626977-e0b5f29c104d4dc16198e1cf34877b7c2652650abe588c347f07a05b363ab5af

Artificial_Till Token:
* Name: artificial_till_token
* Token: xapp-1-A06LFQ6JHSP-6718738992768-9630b3c476f7b4fae5ba5e429a231c4ed86f9368d1c1288039fc420f3031f1c7

#### Enable event subscriptions ✅

Artificial_Till subscribed to 
* app_mention
* message.im - A message was posted in a direct message channel. Maybe that's what I need to get the entire history of the channel...

#### Install the Slackbot in a workspace ✅

Till_AI:
* Bot User OAuth Token: xoxb-6689143819638-6689176192422-tniX9UKom5L15tw3tSdqLXQF
* To be used as SLACK_BOT_TOKEN later

Ar6tificial_Till:
* Bot User Oath Token: xoxb-6689143819638-6681398560231-Ygof6ApX9LdS7CObLs2oMXwU

#### Set Up the Python Project ✅

#### Coding to run the Slackbot ✅

#### Testing the Slackbot ✅

### 2024-02-24 Continuiong from there

* Took this [ChatGPT class](https://gist.github.com/joeddav/a11e5cc0850f0e540324177a53b547ae)



