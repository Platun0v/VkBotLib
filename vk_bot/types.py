import json


class Message:
    @classmethod
    def from_json(cls, json_string):
        obj = json.loads(json_string)

        return cls(obj)

    def __init__(self, message_id, date, peer_id, from_id, text, ref, ref_source, attachments, geo, payload,
                 fwd_messages, reply_messages, action):
        self.message_id = message_id
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
