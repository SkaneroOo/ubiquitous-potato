import socket
import threading
import sys


#192.168.56.1:52222

class Client:
	

	def sendMsg(self, sock):
		while True:
			sock.send(bytes(str([self.name, input()]), 'utf-8'))

	def __init__(self, address):
		name = input('Username: ')
		self.name = name
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((address, 19896))

		iThread = threading.Thread(target=self.sendMsg, args=(sock,))
		iThread.daemon = True
		iThread.start()

		while True:
			data = sock.recv(5120)
			if not data:
				break
			data = str(data, 'utf-8')
			data = eval(data)
			user, data = data[0], data[1]
			if user != self.name:
				if len(user)>7:
					user += '\t'
				else:
					user += '\t\t'
				print(user + str(data))



client = Client('2.tcp.eu.ngrok.io')
