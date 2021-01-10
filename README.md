# bellchan
[![CircleCI](https://circleci.com/gh/shirakiya/bellchan.svg?style=svg)](https://circleci.com/gh/shirakiya/bellchan)  
bellchan is my home bot. Using [python-slackclient](https://github.com/slackapi/python-slackclient).


## Abilities
- notification today's Tokyo Dome schedule from [Tokyo Dome schedule](https://www.tokyo-dome.co.jp/dome/event/schedule.html) @ 09:00, 19:00 on every day


## Setup
#### Bots Integration
At first, set `bots` integration in Slack setting page and get `API_TOKEN`.

#### environment variables
Export environment variables.

| name                   | type    | default | description                                         |
|------------------------|---------|---------|-----------------------------------------------------|
| SLACK_API_TOKEN        | string! |         | Slack bot API token                                 |
| DEFAULT_CHANNEL_ID     | string! |         | Slack channel ID used as default                    |
| BOT_ID                 | string! |         | Slack bot user ID                                   |
| HEROKU_API_KEY         | string! |         | Heroku API Key                                      |


## Run App
```
$ docker-compose build
$ docker-compose up
```
