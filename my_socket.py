import socket


class MySocket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print ("Socket successfully created")
        except socket.error as err:
            print ("socket creation failed with error %s" %(err))
        
        self.s.connect((ip, port))
        print ("the socket has successfully connected")
    
    def send(self, message):
        # self.s.connect((self.ip, self.port))
        self.s.send(message.encode())
        
    def close(self):
        self.s.close()
    