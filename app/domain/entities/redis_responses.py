class RedisResponses:
    text: str

    def __init__(self, text: str):
        self.text = text

    def encode(self):
        response = f"+{self.text}\r\n"
        return response.encode()
