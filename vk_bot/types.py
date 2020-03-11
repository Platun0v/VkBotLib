import json
import html


class Message:
    @classmethod
    def from_dict(cls, obj: dict):
        message_id = obj['id']
        date = obj['date']
        peer_id = obj['peer_id']
        from_id = obj['from_id']
        text = obj['text']
        attachments = obj['attachments']
        payload = obj.get('payload', '{}')
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

        text = html.unescape(text)
        self.command = None

        self.text = text
        self.raw_text = text
        self.text_lower = text.lower()

        self.attachments = attachments
        self.payload = json.loads(payload)
        self.payload_command = None
        self.payload_data = None
        if isinstance(self.payload, dict):
            self.payload_command = self.payload.get('command')
            self.payload_data = self.payload.get('data')
        self.fwd_messages = fwd_messages  # TODO: Process forward messages

    def _get_command_from_message(self, command_start):
        if self.text_lower[0] == command_start:
            sep = self.text.find(' ')
            if sep == -1:
                sep = len(self.text)
            self.command = self.text[1:sep]  # Must go first!
            self.text: str = self.text[sep + 1:]
            self.text_lower = self.text.lower()
            return

        self.command = ''

    def process_command(self, command_start):
        # TODO: Проверка, что command_start один символ. Проверка, что комманда является одним словом.
        if self.command is None:
            self._get_command_from_message(command_start)

        return self.command


class Attachments:
    @classmethod
    def from_dict(cls, obj: dict):
        photo = []
        video = []
        audio = []
        doc = []
        link = []
        market = []
        market_album = []
        wall = []
        wall_reply = []
        sticker = []
        gift = []
        for attach in obj:
            if attach['type'] == 'photo':
                photo.append(attach['photo'])
            if attach['type'] == 'video':
                video.append(attach['video'])
            if attach['type'] == 'audio':
                audio.append(attach['audio'])
            if attach['type'] == 'doc':
                doc.append(attach['doc'])
            if attach['type'] == 'link':
                link.append(attach['link'])
            if attach['type'] == 'market':
                market.append(attach['market'])
            if attach['type'] == 'market_album':
                market_album.append(attach['market_album'])
            if attach['type'] == 'wall':
                wall.append(attach['wall'])
            if attach['type'] == 'wall_reply':
                wall_reply.append(attach['wall_reply'])
            if attach['type'] == 'sticker':
                sticker.append(attach['sticker'])

        return cls(photo, video, audio, doc, link, market, market_album, wall, wall_reply, sticker, gift)

    def __init__(self, photo, video, audio, doc, link, market, market_album, wall, wall_reply, sticker, gift):
        self.photo = photo
        self.video = video
        self.audio = audio
        self.doc = doc
        self.link = link
        self.market = market
        self.market_album = market_album
        self.wall = wall
        self.wall_reply = wall_reply
        self.sticker = sticker
        self.gift = gift

    def __bool__(self):
        return self.photo \
               or self.video \
               or self.audio \
               or self.doc \
               or self.link \
               or self.market \
               or self.market_album \
               or self.wall \
               or self.wall_reply \
               or self.sticker \
               or self.gift
