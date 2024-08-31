import socket

from app.util import convert_into_resp

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client, addr = server_socket.accept()
    client.send(convert_into_resp("+PONG\r\n"))

    while True:



if __name__ == "__main__":
    main()
