"""

To run my code, type in "python3 myclient.py localhost 8090", click enter and simply follow the instruction, enter 1, 2, 3, 4 or 5 to choose what actions to take.
Enter 1 to register, after enter 1, enter the name you want to use
Enter 2 to send messages to all registered users, after enter 2, input messages you want to send
Enter 3 to send messages to a specified user, after enter 3, input the name of target user, and then enter the message
Enter 4 to view all users' name who are registered
Enter 5 to quit the protocol
Before running 2 and 3, user must be register first, or fail message will return.
"""

import sys
from ex2utils import Client

import time


class IRCClient(Client):

	def __init__(self):
		super(IRCClient, self).__init__()

	def onStart(self):
		print("Welcome to the system! What do you want to do?\n1. Register\n2. Send to all people\n3. Send to someone\n4. Get the list of registered people\n5. Quit\nInput number to select operations: ")

	def onMessage(self, socket, message):
		# *** process incoming messages here ***
		if "Command is::" in message:
			return True
		elif "Parameter is::" in message:
			return True
		else:
			print(message)
		return True

	def onStop(self):
		sys.exit(1)

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

#send message to the server
option = input()
while option != 5:
	if option == "1":
		registerName = input("Please enter the username: ")
		client.send(("Register " + registerName).encode())
	elif option == "2":
		mess = input("Please enter the message: ")
		client.send(("GroupSend " + mess).encode())
	elif option == "3":
		targetUser = input("Please enter the user you want to sent message: ")
		mess = input("Please enter the message: ")
		client.send(("SingleSend " + targetUser + " " + mess).encode())
	elif option == "4":
		client.send(("RegisterList").encode())
	elif option == "5":
		client.send(("Quit").encode())
		client.stop()
	else:
		print("Please enter a valid number")
	option = input("Input number to select operations: \n")