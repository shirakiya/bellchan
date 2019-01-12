# bellchan
[![CircleCI](https://circleci.com/gh/shirakiya/bellchan.svg?style=svg)](https://circleci.com/gh/shirakiya/bellchan)  
bellchan is my home bot. Using [python-slackclient](https://github.com/slackapi/python-slackclient).


## Abilities
- notification budget from [Money forward](https://moneyforward.com/) @ 12:00 on Sat.
- notification today's Tokyo Dome schedule from [Tokyo Dome schedule](https://www.tokyo-dome.co.jp/dome/event/schedule.html) @ 09:00, 19:00 on every day


## Required
- Python 3.7.1


## Setup
#### Bots Integration
At first, set `bots` integration in Slack setting page and get `API_TOKEN`.


#### Development Setup
```
$ pip install -r requirements-dev.txt

# export environment variables below
```

__environment variables__

| name                   | type    | default | description                                         |
|------------------------|---------|---------|-----------------------------------------------------|
| SLACK_API_TOKEN        | string! |         | Slack bot API token                                 |
| DEFAULT_CHANNEL_ID     | string! |         | Slack channel ID used as default                    |
| BOT_ID                 | string! |         | Slack bot user ID                                   |
| HEROKU_API_KEY         | string! |         | Heroku API Key                                      |
| MONEY_FORWARD_ID       | string! |         | Money forward user ID                               |
| MONEY_FORWARD_PASSWORD | string! |         | Money forward password                              |


## Run App
```
$ python run.py
```
