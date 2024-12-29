class RedisResponses:
    response: bytes

    def __init__(self, text: str):
        response = "+" + text + "\r\n"
        self.response = response.encode()
