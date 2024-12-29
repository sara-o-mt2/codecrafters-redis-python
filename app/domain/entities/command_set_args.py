class CommandSetArgs:
    key: str
    value: str
    expiry: bool
    interval: int # milliseconds

    def __init__(self, args: list[str]):
        self.key = args[0]
        self.value = args[1]
        if len(args) == 4 and args[2] == "px" and args[3].isnumeric():
            self.expiry = True
            self.interval = int(args[3])
        else:
            self.expiry = False
            self.interval = 0
