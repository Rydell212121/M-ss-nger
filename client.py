import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8081))


def client(server):
    fin_mark = b"\r\n\r\n"
    end_mark = b"\r\n"
    while True:
        try:
            text = input("Введите сообщение, для выхода нажмите ctrl + c: ")
        except KeyboardInterrupt:
            server.sendall(fin_mark)
            return True
        server.sendall(text.encode("utf-8") + end_mark) 
        text = b""
        while True:
            data = server.recv(1024)
            text += data
            if data.endswith(fin_mark):
                return True
            elif data.endswith(end_mark):
                print(data.decode("utf-8"))
                return False



while True:
    if client(s):
        break

s.close()