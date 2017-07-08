from slackbot.bot import respond_to


@respond_to(r'.+')
def respond(message):
    text = message.body['text']
    message.send(f'{text} バファローベルだよ！')
