class RedisResponses:
    text: str

    def __init__(self, text: str | None = None):
        self.text = text

    def encode(self):
        if self.text is None:
            response = "$-1\r\n"
        else:
            response = f"+{self.text}\r\n"
        return response.encode()
