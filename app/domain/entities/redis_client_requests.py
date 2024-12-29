from app.domain.values.data_type import RESPDataType

class RedisClientRequests:
    msg: bytes
    initial_pos_value: int

    def __init__(self, msg: bytes):
        self.msg = msg
        self.initial_pos_value = 4
    def isEmpty(self):
        return len(self.msg) == 0
    def decode_bulk_string(self, msg=None):
        if msg is None:
            msg = self.msg
        if msg[0:1] == b"$":
            lines = msg[1:].splitlines()
            if int(lines[0]) == len(lines[1]):
                return lines[1].decode("utf-8")
        return None
    def decode_array(self, msg=None):
        if msg is None:
            msg = self.msg
        elements_count = msg[1:].splitlines()[0]
        start = self.initial_pos_value
        end = self.initial_pos_value
        elements = []
        for next_element in range(int(elements_count)):
            next_element_size_value = int(msg[start + 1 :].splitlines()[0])
            next_element_size_len = str(next_element_size_value).__len__() + 1
            end = start + next_element_size_len + 2 + next_element_size_value
            elements.append(self.decode(msg[start:end]))
            start = end + 2
        return elements
    def decode(self, msg=None):
        if msg is None:
            msg = self.msg
        msg_first_byte = msg[0:1]
        match msg_first_byte:
            case RESPDataType.SIMPLE_STRING.value:
                pass
            case RESPDataType.ERROR.value:
                pass
            case RESPDataType.INTEGER.value:
                pass
            case RESPDataType.BULK_STRING.value:
                return self.decode_bulk_string(msg)
            case RESPDataType.ARRAY.value:
                return self.decode_array(msg)
            case _:
                return None
