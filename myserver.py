import sys
from ex2utils import Server

class MyServer(Server):

	def __init__(self):
		super(MyServer, self).__init__()
		self.currentConnections = 0
		self.registerList = {}

	def onStart(self):
		print("My server has started")
		
	def onMessage(self, socket, message):
		# This function takes two arguments: 'socket' and 'message'.
		#     'socket' can be used to send a message string back over the wire.
		#     'message' holds the incoming message string (minus the line-return).
	
		# convert the string to an upper case version
		#message = message.upper()

		# Just echo back what we received
		#message=message.encode()
		command, sep, parameter = message.strip().partition(' ')
		socket.send(("Command is:: " + command).encode())
		socket.send(("Parameter is:: " + parameter).encode())
		if command == "Register":
			if parameter in self.registerList.keys():
				socket.send(("Already used, please change another one").encode())
			else:	
				self.registerList[parameter] = socket
				socket.send(("Register success!").encode())

		elif command == "GroupSend":
			if socket in self.registerList.values():
				for everySocket in self.registerList.values():
					if socket != everySocket:
						everySocket.send((list(self.registerList.keys())[list(self.registerList.values()).index(socket)] + ": " + parameter).encode())
				socket.send(("Message sent!").encode())
			else:
				socket.send(("Please register first").encode())

		elif command == "SingleSend":
			if socket in self.registerList.values():
				target, sep, mess = parameter.strip().partition(' ')
				if target in self.registerList:
					self.registerList[target].send((list(self.registerList.keys())[list(self.registerList.values()).index(socket)] + ": " + mess).encode())
					socket.send(("Message sent!").encode())
				else:
					socket.send(("Can't find target user").encode())
			else:
				socket.send(("Please register first").encode())

		elif command == "RegisterList":
			nameList = ""
			if len(self.registerList) != 0:
				for i in self.registerList.keys():
					nameList += i + "\n"
			else:
				nameList = "No registered users"
			socket.send(nameList.encode())

		elif command == "Quit":
			socket.send(("Thank you for using the protocol").encode())
			socket.close()
		else:
			socket.send(("Not a valid command").encode())
		
		# Signify all is well
		return True

	def onStop(self):
		print("Server closed")
		self.registerList.clear()
		sys.exit(1)

	def onConnect(self, socket):
		self.currentConnections += 1
		print("Current number of connections: ", str(self.currentConnections))

	def onDisconnect(self, socket):
		self.currentConnections -= 1
		self.registerList.pop(list(self.registerList.keys())[list(self.registerList.values()).index(socket)])
		print("Current number of connections: ", str(self.currentConnections))

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

# Start server
server.start(ip, port)

