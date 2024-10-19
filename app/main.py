import socket

from app.util import convert_into_resp

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client, addr = server_socket.accept()

    while True:
        request = client.recv(512)
        data_lines = request.decode().split('\n')

        for data in data_lines:
            print(data)
            if "ping" in data.lower():
                client.send(convert_into_resp("+PONG\r\n"))


if __name__ == "__main__":
    main()
