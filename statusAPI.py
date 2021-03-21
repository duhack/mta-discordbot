#AUTHOR: duhack
#GITHUB: https://github.com/duhack
#WWW: https://duhack.pl/ 

import socket

class checkSerwer:
    game = None
    port = None
    name = None
    gamemode = None
    map = None
    version = None
    somewhat = None
    players = None
    maxplayers = None
    returns = {}
    def __init__(self, address: str, port: int = 22003, **kwargs):
        self.address = address
        self.port = port
        self.response = None
        self.polacz(address, port)
        self.returns = {}

    def przetworz(self, start):
        start_end = start + 1
        length = ord(self.response[start:start_end]) - 1
        value = self.response[start_end:start_end + length]
        return start_end + length, value.decode('utf-8')

    def wyswietl(self, decode):
        params = ('game', 'port', 'name', 'gamemode', 'map', 'version', 'somewhat', 'players', 'maxplayers')
        start=4
        for param in params:
            start, value = self.przetworz(start)
            setattr(self, param, value)
        for title in self.returns:
            print(title, " - ", self.returns[title])

    def polacz(self, address, port):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #tworzy socket
        serversocket.settimeout(5) #nadaje timeout
        serversocket.connect((address, port+123)) #łączy się z serwerem
        serversocket.send(b"s") #wysyla zapytanie
        self.response = serversocket.recv(16384) #odbiera informacje
        decoded = self.response.decode('utf-8') #dekoduje
        self.wyswietl(decoded) #przekazuje dane do wyswietlenia
        serversocket.close() #zamyka polaczenie


