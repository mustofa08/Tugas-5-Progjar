import socket
import threading
from http import HttpServer

httpserver = HttpServer()
rcv = b""  # Gunakan bytes untuk rcv

class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        global rcv
        try:
            data = self.client_socket.recv(1024)
            if data:
                rcv += data
                if rcv.endswith(b'\r\n\r\n'):
                    response = httpserver.proses(rcv.decode())
                    if isinstance(response, str):
                        response = response.encode()
                    self.client_socket.sendall(response)
                    rcv = b""
        except Exception as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            self.client_socket.close()

def main():
    host = '0.0.0.0'
    port = 60001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server berjalan di {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Terhubung dengan client {client_address}")
            ClientThread(client_socket, client_address).start()
    except KeyboardInterrupt:
        print("\nServer dihentikan")
        server_socket.close()

if __name__ == "__main__":
    main()
