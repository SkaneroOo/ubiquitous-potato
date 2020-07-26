import socket
import socketserver
import threading
import sys
import time
import random

#class Server:
#	
#	connections = []
#
#	def __init__(self):
#		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		sock.bind(('localhost', 10000))
#		sock.listen(1)
#
#		while True:
#			c, a = sock.accept()
#			cThread = threading.Thread(target=self.handler, args=(c,a))
#			cThread.daemon = True
#			cThread.start()
#			self.connections.append(c)
#			print(str(a[0]) + ':' + str(a[1]) + 'connected')
#
#	def handler(self, c, a):
#		while True:
#			data = c.recv(5120)
#			for connection in self.connections:
#				connection.send(bytes(data))
#			if not data:
#				print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
#				self.connections.remove(c)
#				c.close()
#				break

connections = []

class Handler(socketserver.BaseRequestHandler):

	def handle(self):
		global connections
		connections.append(self.request)
		c = self.request
		while True:
			data = self.request.recv(1024).decode()
			if not data:
				connections.remove(c)
				c.close()
				break
			if data[0] == '🅂':
				pass
			elif data[0] == '/':
				self.command(data)
			else:
				#print('data received:', data)
				#response = str(random.randint(1,432787843))
				#print('response:', response)
				for connection in connections:
					connection.sendall(data.encode())
		
	def command(self, cmd):
		print(cmd)
		args=cmd.strip('/').split()
		if args[0].upper() == 'JOIN':
			u = cmd[6:]
			self.name = u
			m = 'New user on server: ' + u
			for connection in connections:
				connection.sendall(m.encode())

class BetterServer:
	connections = []
	def __init__(self):
		server = socketserver.ThreadingTCPServer(('localhost', 10000), Handler)
		server.serve_forever()





server = BetterServer()