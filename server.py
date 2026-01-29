import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 8081))
s2.bind(("127.0.0.1", 8082))
s.listen(1)
s2.listen(1)

print("Server started...")


def talk(conn: socket.socket, conn2: socket.socket) -> bool:
    """Реализует "разговор" между двумя клиентами, если один из клиентов обрывает связь
    возвращает True, если все хорошо возвращает False. Разговор ведется по очереди, причем
    первым клиентом должен быть именно conn. conn и conn2 сокеты клиентов."""

    fin_mark = b"\r\n\r\n"
    end_mark = b"\r\n"

    text = b""
    while True:
        data = conn.recv(1024)
        text += data
            
        if data.endswith(fin_mark):
            conn2.sendall(b"user disconnected" + fin_mark)
            return True
            
        elif data.endswith(end_mark):
            conn2.sendall(text)

            text2 = b""
            while True:
                data2 = conn2.recv(1024)
                text2 += data2
  
                if data2.endswith(fin_mark):
                    conn.sendall(b"user disconnected" + fin_mark)
                    return True
                    
                elif data2.endswith(end_mark):
                    conn.sendall(text2)
                    return False


while True:
    conn, addr = s.accept()
    conn2, addr2 = s2.accept()

    while not talk(conn, conn2):
        continue
    break

conn.close()
s.close()
conn2.close()
s2.close()
print("server stopped by the client")
