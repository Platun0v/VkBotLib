import json


class Message:
    @classmethod
    def from_dict(cls, obj: dict):
        message_id = obj['id']
        date = obj['date']
        peer_id = obj['peer_id']
        from_id = obj['from_id']
        text = obj['text']
        attachments = obj['attachments']
        payload = '{}'
        if 'payload' in obj.keys():
            payload = obj['payload']
        fwd_messages = ['fwd_messages']

        return cls(message_id, date, peer_id, from_id, text, attachments, payload,
                   fwd_messages, obj)

    def __init__(self, message_id, date, peer_id, from_id, text, attachments, payload,
                 fwd_messages, raw=None):
        self.raw = raw

        self.id = message_id
        self.date = date
        self.peer_id = peer_id
        self.from_id = from_id
        self.text = text
        self.attachments = attachments  # TODO: Attachments class
        self.payload = json.loads(payload)
        self.fwd_messages = fwd_messages  # TODO: Process forward messages
