# bellchan

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
| MONEY_FORWARD_ID       | string! |         | [Money forward](https://moneyforward.com/) user ID  |
| MONEY_FORWARD_PASSWORD | string! |         | [Money forward](https://moneyforward.com/) password |

## Run App
```
$ python run.py
```
