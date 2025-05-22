import socket
import threading
import os

from _signal_ import Signal

class Server:
    def __init__(self, host: str = "", port: int = 0):
        self.host = host
        self.port = port
        self.clients = []
        
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False

        self.server_started = Signal()
        self.server_stopped = Signal()
        
        self.client_connected = Signal()
        self.client_disconnected = Signal()

    def start(self):
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        self.running = True

        

        self.server_started.emit()
        
        threading.Thread(target=self._accept_clients, daemon=True).start()

    def _accept_clients(self):
        while self.running:
            client_sock, addr = self.server_sock.accept()
            self.clients.append(client_sock)
            
            self.client_connected.emit()
            

            threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True).start()

    def _handle_client(self, client_sock: socket.socket):
        while self.running:
            try:
                data = client_sock.recv(1024)
                if not data:
                    break
                self.broadcast(data, sender=client_sock)
            except:
                break
        if client_sock in self.clients:
            self.clients.remove(client_sock)

        self.client_disconnected.emit()

        client_sock.close()

    def broadcast(self, data: bytes, sender: socket.socket = None):
        for c in list(self.clients):
            if c is not sender:
                try:
                    c.send(data)
                except:
                    self.clients.remove(c)

    def stop(self):
        self.running = False
        self.server_sock.close()
        for c in list(self.clients):
            c.close()
            
        self.server_stopped.emit()

class Client:
    def __init__(self, host: str = "", port: int = 5000):
        self.host = host
        self.port = port
        self.server : Server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        
        self.connected = Signal()
        self.disconnected = Signal()

        self.connection_timeout = Signal()

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.running = True
        
    def send(self, data: bytes):
        if self.running:
            self.sock.send(data)

    def receive(self, callback):
        def _recv_loop():
            while self.running:
                try:
                    data = self.sock.recv(1024)
                    if not data:
                        break
                    callback(data)
                except:
                    break
            self.running = False
        threading.Thread(target=_recv_loop, daemon=True).start()

    def disconnect(self):
        self.running = False
        self.sock.close()
        print("disconnected")
        
        
        
        
        
        
if __name__ == "__main__":
    while True:
        i = input("host or join\n> ")
        if i in ["host", "join"]:
            break
        
    addr = input("ip=")
    port = int(input("port="))
    s = Server(
        host=addr,
        port=port
    )
    
    c = Client(
        host=addr,
        port=port
    )
    c.server = s
    
    def handle_msg(data):
        print(f"[remote]: {data.decode()}")
    
    def _whilechat_():
        while True:
            msg = input("> ")
            if len(msg) > 0 and msg[0] == "/":
                cmd = msg.removeprefix("/")
                class Command:
                    def __init__(self, id: str, *description: str, callback: any):
                        self.id = id
                        self.description = description
                        self.callback = callback
                    
                    def call(self):
                        self.callback()
                
                class Commands:
                    def _help_() -> None:
                        for _cmnd in commands:
                            print(f"{_cmnd.id}: {_cmnd.description}")
                    _help = Command(
                        "help",
                        "Prints a list of commands",
                        callback=_help_
                    )
                            
                    def _peers_():
                        print(c.server.clients)
                    _peers = Command(
                        "peers",
                        "Prints a list of connected peers",
                        callback=_peers_
                    )
                    
                
                commands : list[Command] = [
                    Commands._help,
                    Commands._peers
                ]
                
                for _cmnd in commands:
                    if _cmnd.id == cmd:
                        print(f"[{cmd}] == [{_cmnd.id}]")
                        cmd = _cmnd

                        _cmnd.call()
                        
                        break
                
            else:
                c.send(msg.encode())
        
    
    match i:
        case "host":
            print("starting the server")
            s.start()
            c.connect()

            
            c.receive(handle_msg)
            try:
                _whilechat_()
            except KeyboardInterrupt:
                print("shutting down")
                for _client_ in s.clients:
                    _client_.close()
                
                s.stop()
                c.disconnect()

            
        case "join":
            c.connect()

            c.receive(handle_msg)
            
            try:
                _whilechat_()
            except KeyboardInterrupt:
                c.send(f"{c.sock} disconnected".encode())
                c.disconnect()
