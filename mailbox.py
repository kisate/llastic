import socket, threading

class MessageHandler():
    def __init__(self):
        self.state = 0
        self.message = []
    
    def updateMessage(self, message):
        self.message = message
        self.state = message[0]
        print("in handler : " + str(message) + " " + str(self.state))
        self.processMessage()
        self.state = 0
    
    def processMessage(self):
        return

class Client():

    def __init__(self, host, port):

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception:
            pass
    
    def reader(self, s):
        while self.on:    
            message = []

            part = s.recv(1)
            
            message_size = int.from_bytes(part, byteorder='big')

            for i in range(message_size):
                part = s.recv(8)
                message.append(int.from_bytes(part, byteorder='big', signed=True))

            print ("message")
            
            if (len(message) > 0) : self.messageHandler.updateMessage(message)
            
            if len(part) == 0 : break


    def connect(self, messageHandler):
        self.socket.connect((self.host, self.port))
        self.on = True

        self.messageHandler = messageHandler
        threading.Thread(target=self.reader, args=(self.socket,)).start()

    def send(self, *args):
        
        try : 

            msg = len(args).to_bytes(1, byteorder='big')

            for a in args:
                msg += (a).to_bytes(8, byteorder='big', signed = True)

            print(msg)

            self.socket.send(msg)

        except BaseException as e :
            print (e)

    def disconnect(self):
        self.on = False
        self.socket.close()

class Server():

    def __init__(self, port):
        self.port = port
        
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try : 
            self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception:
            pass

        self.listening_socket.bind(('', port))
        self.listening_socket.listen(5)
    
    def reader(self, s):
        while self.on:    
            message = []

            part = s.recv(1)
            
            message_size = int.from_bytes(part, byteorder='big')

            for i in range(message_size):
                part = s.recv(8)
                message.append(int.from_bytes(part, byteorder='big', signed=True))

            print (message)
            
            self.messageHandler.updateMessage(message)
            
            if len(part) == 0 : break


    def accept(self, messageHandler):
        
        self.conn, addr = self.listening_socket.accept()
        print("{} connected".format(addr))
        
        self.on = True

        self.messageHandler = messageHandler
        threading.Thread(target=self.reader, args=(self.conn,)).start()

    def send(self, *args):
        
        try : 

            msg = len(args).to_bytes(1, byteorder='big')

            for a in args:
                msg += (a).to_bytes(8, byteorder='big', signed = True)

            print(msg)

            self.conn.send(msg)

        except BaseException as e :
            print (e)

    def close(self):
        self.on = False
        self.conn.close()
        self.listening_socket.close()