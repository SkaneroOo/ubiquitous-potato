import socket
import threading
import sys
from tkinter import *
import json

username = ''
ip = ''
client = None

with open('./Client/latest.json') as json_file:
	latest = json.load(json_file)

def addd(new_data):
	global latest
	if new_data in latest:
		pass
	else:
		if len(latest) == 10:
			latest.remove(latest[-1])
		latest = [new_data] + latest
		with open('./Client/latest.json', 'w') as outfile:
			json.dump(latest, outfile)




class con:

	def __init__(self):
		self.root = Toplevel(window)
		self.root.geometry('250x250')
		self.root.title('Connection')
		Label(self.root, text='Username', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=40, y=30)
		n = StringVar()
		self.Name=Entry(self.root, text=n)
		self.Name.place(x=40, y=60)
		Label(self.root, text='Server IP', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=40, y=90)
		i = StringVar()
		self.IP=Entry(self.root, text=i)
		self.IP.place(x=40, y=120)
		Button(self.root, text='Confirm', bg='#F0F8FF', font=('arial', 12, 'normal'), command=self.send).place(x=70, y=150)
		self.root.mainloop()
	
	def send(self):
		global username
		global ip
		global client
		username = self.Name.get()
		ip = self.IP.get()
		username = username.strip()
		ip = ip.strip()
		if ((len(username) > 0) and (len(ip) > 0)):
			client = Client(ip, username)
			print('Connected to {} as {}.'.format(ip, username))
			messages.insert(INSERT, 'Connected to {} as {}.\n\n'.format(ip, username))
			messages.see(END)
			client.sendMsg('joined the chat.')
			addd((ip, username))
			self.root.destroy()
			#threading.Thread(target=client.work)

def recon(conn):
	global client
	client = Client(conn[0], conn[1])
	print('Connected to {} as {}.'.format(conn[0], conn[1]))
	messages.insert(INSERT, 'Connected to {} as {}.\n\n'.format(conn[0], conn[1]))
	client.sendMsg('joined server')
	messages.see(END)


window = Tk()
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)
sb = Scrollbar(window) 
messages = Text(window)
sb.pack(side = RIGHT, fill = Y)
messages.pack()


sb.config( command = messages.yview )

menubar = Menu(window)

menubar.add_command(label="Connect", command=con)
if len(latest) > 0:
	reco = Menu(menubar, tearoff=0)
	for item in latest:
		reco.add_command(label='As {} to {}'.format(item[1], item[0]), command=lambda: recon(item))
	menubar.add_cascade(label="Reconnect", menu=reco)
menubar.add_command(label="Exit", command=window.quit) 
window.config(menu=menubar) 

#input_user = StringVar()
#input_field = Entry(window, text=input_user)
#input_field.pack(side=BOTTOM, fill=X)

def Enter_pressed(event):
	input_get = input_field.get()
	input_user.set('')
	input_get = input_get.strip()
	if len(input_get) > 0:
		client.sendMsg(input_get)
		#messages.insert(INSERT, '%s\n' % input_get)
		messages.see(END)
		return "break"

frame = Frame(window)
input_field.bind("<Return>", Enter_pressed)
frame.pack()



class Client:
	

	def sendMsg(self, mes):
		self.sock.send(bytes(str([self.name, mes]), 'utf-8'))

	def __init__(self, address, username):
		self.name = username
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		address, port = address.split(':')
		self.sock.connect((address, int(port)))

		iThread = threading.Thread(target=self.work)
		iThread.daemon = True
		iThread.start()

	def work(self):
		while True:

			data = self.sock.recv(1024)
			if not data:
				break
			data = str(data, 'utf-8')
			data = eval(data)
			user, data = data[0], data[1]
			if len(user)>7:
				user += '\t'
			else:
				user += '\t\t'
			messages.insert(INSERT, user + str(data) + '\n\n')
			messages.see(END)
			#return user + str(data)



#client = Client(address, username)
window.mainloop()
