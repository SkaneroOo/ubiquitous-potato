import socket
import threading
import sys
import asyncio
from discord.ext import commands, tasks
import discord

TOKEN = 'NjI0NjUxMTA5MzYwNzMwMTcx.XxnJ5Q.Q9kojbGtacMcMxfhMPxUlMRJGH0'
BOT_PREFIX=('w.', 'W.')
bot = commands.Bot(command_prefix = BOT_PREFIX)

#192.168.56.1:52222

class Client:
	

	def sendMsg(self, sock):
		while True:
			sock.send(bytes(str([self.name, input()]), 'utf-8'))

	def __init__(self, address, name):
		self.name = name
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((address, 10000))

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

@bot.event
async def on_message(message):
	client = Client('192.168.56.1', message.author.display_name)

client = Client('192.168.56.1')
bot.run(TOKEN)
