class RESPCommand:
    command: str
    arguments: list[str]

    def __init__(self, decoded_msg: list[str]):
        self.command = decoded_msg[0]
        self.arguments = []
        for arg in decoded_msg[1:]:
            self.add_argument(arg)

    def add_argument(self, argument: str):
        self.arguments.append(argument)

    def __repr__(self):
        return self.command, self.arguments

    def __str__(self):
        return f"{self.command} {' '.join(self.arguments)}"

    def __iter__(self):
        yield self.command
        yield self.arguments
