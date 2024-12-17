import socket
import threading

from app.util import convert_into_resp

def handle_client(client: socket.socket, addr: tuple[str, int]) -> None:
    with client:
        while True:
            request = client.recv(512)
            data_lines = request.decode().split('\n')

            for data in data_lines:
                if "ping" in data.lower():
                    client.send(convert_into_resp("+PONG\r\n"))

def main():
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
