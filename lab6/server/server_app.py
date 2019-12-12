import socket
import json

def start():
    serv_socket = socket.socket()
    serv_socket.bind(('', 9005))
    serv_socket.listen(1)

    print("Server started")
    while True:
        conn, addr = serv_socket.accept()
        print("Connected: ", addr)

        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        data = data.lower()

        result = dict()
        for ch in data:
            if result.get(ch) is None:
                result[ch] = 0
            result[ch] += 1

        conn.send(json.dumps(result).encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    start()
