import socket
import threading

from app.domain.entities.redis_client_requests import RedisClientRequests
from app.domain.entities.redis_responses import RedisResponses
from app.domain.entities.resp_command import RESPCommand


def handle_client(client: socket.socket, addr: tuple[str, int]) -> None:
    with client:
        while True:
            row_requests = client.recv(512)
            if not row_requests:
                break

            requests = RedisClientRequests(row_requests)
            command = RESPCommand(requests.decode())

            if command.command == "PING":
                client.send(RedisResponses("PONG"))
            elif command.command == "ECHO":
                client.send(RedisResponses(command.arguments[0]))

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
