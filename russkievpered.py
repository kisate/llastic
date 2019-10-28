import sender
from mailbox import Client, MessageHandler
host = '192.168.43.83'
port = 6166 # fix number

client = Client(host,port)
messagehandler = sender.MyMessageHandler()
print("connecting")
client.connect(messagehandler)
print("connected")

client.send(3)