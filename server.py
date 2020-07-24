import socket
import threading
import sys
import time


class Server:
	
	connections = []

	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost', 10000))
		sock.listen(1)

		while True:
			c, a = sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]) + 'connected')

	def handler(self, c, a):
		while True:
			data = c.recv(5120)
			for connection in self.connections:
				connection.send(bytes(data))
			if not data:
				print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
				self.connections.remove(c)
				c.close()
				break


server = Server()