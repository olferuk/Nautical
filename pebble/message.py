
CAPTION_ABOVE = 0
CAPTION_BELOW = 1

class Message():
    def __init__(self,
                 message: str = None,
                 image: str = None,
                 image_url: str = None,
                 message_media_relation: int = CAPTION_ABOVE,
                 buttons: list = None,
                 meta: str = ''
                ):
        self.message = message
        self.image = image
        self.image_url = image_url
        self.message_media_relation = message_media_relation
        self.buttons = buttons
        self.meta = meta

    def __repr__(self):
        return ('MESSAGE: {0}\n'
                'IMAGE: {1}\n'
                'URL: {2}\n'
                'BUTTONS: {3}\n'
                'META: {4}').format(self.message,
                                    self.image,
                                    self.image_url,
                                    self.buttons,
                                    self.meta)
