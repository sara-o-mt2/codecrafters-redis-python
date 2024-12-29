import socket, time
import threading

from app.domain.entities.redis_client_requests import RedisClientRequests
from app.domain.entities.redis_responses import RedisResponses
from app.domain.entities.resp_command import RESPCommand
from app.domain.entities.command_set_args import CommandSetArgs


table_store = {}
table_expiry = {} 

def handle_client(client: socket.socket, addr: tuple[str, int]) -> None:
    with client:
        row_requests = client.recv(512)
        if not row_requests:
            return

        requests = RedisClientRequests(row_requests)
        command = RESPCommand(requests.decode())

        if command.command == "PING":
            response = RedisResponses("PONG")
            client.send(response.encode())
        elif command.command == "ECHO":
            response = RedisResponses(command.arguments[0])
            client.send(response.encode())
        elif command.command == "SET":
            command_set_args = CommandSetArgs(command.arguments)
            table_store[command_set_args.key] = command_set_args.value
            if command_set_args.expiry:
                table_expiry[command_set_args.key] = time.time() * 1000 + command_set_args.interval
            response = RedisResponses("OK")
            client.send(response.encode())
        elif command.command == "GET":
            if command.arguments[0] in table_expiry:
                if table_expiry[command.arguments[0]] < time.time() * 1000:
                    table_store.pop(command.arguments[0], None)
                    table_expiry.pop(command.arguments[0], None)
                    response = RedisResponses("$-1")
                    client.send(response.encode())
                    return

            response = RedisResponses(table_store.get(command.arguments[0]))
            client.send(response.encode())
        else:
            return

def main() -> None:
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        try:
            client, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=[client, addr]
            )
            client_thread.start()
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    main()
