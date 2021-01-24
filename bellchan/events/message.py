class Message:
    """
    # Message with mention
    {
        'blocks': [{
            'block_id': 'IIYA4',
            'elements': [{
                'elements': [
                    {
                        'type': 'user',
                        'user_id': 'U65Q8QCM6',
                    },
                    {
                        'text': ' ping',
                        'type': 'text',
                    },
                ],
                'type': 'rich_text_section',
            }],
            'type': 'rich_text',
        }],
        'channel': 'C67RZ7PT4',
        'client_msg_id': 'f5a0a5e7-ecd3-473f-85f6-fc6a3d44a9c5',
        'event_ts': '1611479956.000400',
        'source_team': 'T04D07KQE',
        'suppress_notification': False,
        'team': 'T04D07KQE',
        'text': '<@U65Q8QCM6> ping',
        'ts': '1611479956.000400',
        'user': 'U04D07KQG',
        'user_team': 'T04D07KQE',
    }

    # Edited message with mention
    {
        'channel': 'C67RZ7PT4',
        'event_ts': '1611482370.007000',
        'hidden': True,
        'message': {
            'blocks': [{
                'block_id': 't7+F',
                'elements': [{
                    'elements': [
                        {
                            'type': 'user',
                            'user_id': 'U65Q8QCM6',
                        },
                        {
                            'text': ' aaa',
                            'type': 'text',
                        },
                ],
                'type': 'rich_text_section',
            }],
            'type': 'rich_text'}],
            'client_msg_id': 'cb532f72-3556-4cbf-8d4a-3b9c9e90d91a',
            'edited': {'ts': '1611482370.000000',
                       'user': 'U04D07KQG'},
            'parent_user_id': 'U04D07KQG',
            'source_team': 'T04D07KQE',
            'team': 'T04D07KQE',
            'text': '<@U65Q8QCM6> pinghogehoge',
            'thread_ts': '1611481938.005000',
            'ts': '1611482242.005900',
            'type': 'message',
            'user': 'U04D07KQG',
            'user_team': 'T04D07KQE',
        },
        'previous_message': {
            'blocks': [{
                'block_id': 'Z+Rb',
                'elements': [{
                    'elements': [
                        {
                            'type': 'user',
                            'user_id': 'U65Q8QCM6',
                        },
                        {
                            'text': ' ping',
                            'type': 'text',
                        },
                    ],
                    'type': 'rich_text_section',
                }],
                'type': 'rich_text',
            }],
            'client_msg_id': 'cb532f72-3556-4cbf-8d4a-3b9c9e90d91a',
            'parent_user_id': 'U04D07KQG',
            'team': 'T04D07KQE',
            'text': '<@U65Q8QCM6> ping',
            'thread_ts': '1611481938.005000',
            'ts': '1611482242.005900',
            'type': 'message',
            'user': 'U04D07KQG',
        },
        'subtype': 'message_changed',
        'ts': '1611482370.007000',
    },
    """
    def __init__(self, bot_id: str, raw_data: dict):
        self.bot_id = bot_id
        self.raw_data = raw_data
        self.is_message_changed = False

        self.channel = ''
        self.event_ts = ''
        self.team = ''
        self.text = ''

        if (subtype := raw_data.get('subtype')) and subtype == 'message_changed':
            self.is_message_changed = True

        for k in ('channel', 'event_ts'):
            v = raw_data[k]
            setattr(self, k, v)

        if self.is_message_changed:
            message = raw_data['message']
        else:
            message = raw_data

        for k in ('team', 'text'):
            v = message[k]
            setattr(self, k, v)

    def is_in_dm_channel(self) -> bool:
        return self.channel.startswith('D')

    def is_asked(self) -> bool:
        return f'<@{self.bot_id}>' in self.text

    def is_mentioned(self) -> bool:
        return self.is_asked() or self.is_in_dm_channel()

    def is_edited(self) -> bool:
        return self.is_message_changed
