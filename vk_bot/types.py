import json


class Message:
    @classmethod
    def from_json(cls, json_string):
        obj = json.loads(json_string)

        message_id = obj['id']
        date = obj['date']
        peer_id = obj['peer_id']
        from_id = obj['from_id']
        text = obj['text']
        ref = ['ref']
        ref_source = obj['ref_source']
        attachments = obj['attachments']
        geo = obj['geo']
        payload = obj['payload']
        fwd_messages = ['fwd_messages']
        reply_messages = obj['reply_messages']
        action = obj['action']

        return cls(message_id, date, peer_id, from_id, text, ref, ref_source, attachments, geo, payload,
                   fwd_messages, reply_messages, action, obj)

    def __init__(self, message_id, date, peer_id, from_id, text, ref, ref_source, attachments, geo, payload,
                 fwd_messages, reply_messages, action, raw=None):
        self.raw = raw

        self.id = message_id
        self.date = date
        self.peer_id = peer_id
        self.from_id = from_id
        self.text = text
        self.ref = ref
        self.ref_source = ref_source
        self.attachments = attachments  # TODO: Attachments class
        self.geo = geo
        self.payload = json.loads(payload)
        self.fwd_messages = fwd_messages  # TODO: Process forward messages
        self.reply_messages = reply_messages
        self.action = action
