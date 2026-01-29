import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8082))


def client(server):
    while True:
        text = b""
        while True:
            data = server.recv(1024)
            text += data
            if data.endswith(b"\r\n\r\n"):
                return True
            elif data.endswith(b"\r\n"):
                print(data.decode("utf-8"))
                break
        try:
            text = input("Введите сообщение, для выхода нажмите ctrl + c: ")
        except KeyboardInterrupt:
            server.sendall(b"\r\n\r\n")
            return True
        server.sendall(text.encode("utf-8") + b"\r\n")


while not client(s):
    ...

s.close()