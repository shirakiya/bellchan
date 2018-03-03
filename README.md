# bellchan
bellchan is my home bot. Using [python-slackclient](https://github.com/slackapi/python-slackclient).


## Abilities
- notification budget from [Money forward](https://moneyforward.com/) @ 12:00 on Sat.
- notification today's Tokyo Dome schedule from [Tokyo Dome schedule](https://www.tokyo-dome.co.jp/dome/event/schedule.html) @ 09:00, 19:00 on every day
- notification coin assets


## Required
- Python >= 3.6


## Setup
#### Bots Integration
At first, set `bots` integration in Slack setting page and get `API_TOKEN`.


#### Development Setup
```
$ pip install -r requirements.txt

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
| ZAIF_API_KEY           | string! |         | ZAIF API key                                        |
| ZAIF_API_SECRET        | string! |         | ZAIF API secret                                     |


## Run App
```
$ python run.py
```
