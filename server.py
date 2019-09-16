#Server
import pickle
import socket

packetToSend = {
		"seqNo":12344,
		"ackNo":0,
		"syn":False,
		"fin":False,
		"ack":False,
		"rst":False,
		"psh":False,
		"urg":False,
		"data":"some data"
		}

def resetPacket():

	packetToSend["syn"] = False
	packetToSend["ack"] = False
	packetToSend["fin"] = False
	packetToSend["rst"] = False
	packetToSend["psh"] = False
	packetToSend["urg"] = False


def synRcvd(packetReceived):

	packetToSend["syn"] = True
	packetToSend["ack"] = True
	packetToSend["ackNo"] = packetReceived["seqNo"] + 1

states = ["CLOSED","LISTEN","SYN_RCVD","ESTABLISHED","CLOSE_WAIT","TIME_WAIT","LAST_ACK","CLOSING"]

def checkState(packetReceived,currentState):

	print("Current state is : ",currentState)

	if currentState == states[1]:
		if packetReceived["syn"]:
			currentState = states[2]
			print("State Changed to : ",currentState)
			synRcvd(packetReceived)
			return currentState
		if packetReceived["rst"]:
			currentState = state[0]
			return currentState

	if currentState == states[2]:
		if packetReceived["ack"]:
			currentState = states[3]
			print("State Changed to : ",currentState)
			return currentState

	if currentState == states[3]:
		if packetReceived["fin"]:
			"""
				In case of three way handshake
			"""
			packetToSend["fin"] = True
			packetToSend["ack"] = True
			currentState = states[4]
			print("State changed to : ",currentState)
			return currentState

	if currentState == states[4]:
		if packetReceived["ack"]:
			currentState = states[5]
			print("State changed to : ",currentState)
			print("Waits for 2MSL and state changes to close !!")
			return states[0]

	return currentState

def establishConnection():

	host = socket.gethostname()
	port = 9994
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((host,port))
	serverSocket.listen(5)
	print("Server is listening....")
	clientSocket , addr = serverSocket.accept()
	print("Connected to client : ",addr[0]," : ",addr[1])
	currentState = "LISTEN"

	while True:
		dataReceived = clientSocket.recv(1024)
		packetReceived = pickle.loads(dataReceived)
		print("Packet Received : ",packetReceived)
		currentState = checkState(packetReceived,currentState)

		if currentState == states[0]:
			break

		dataToSend = pickle.dumps(packetToSend)
		clientSocket.send(dataToSend)
		resetPacket()
		print("\n")

	clientSocket.close()
	print("Connection Closed !!!")
	currentState = states[1]

if __name__ == "__main__":

	establishConnection()
  
  
  client
  
  import pickle
import socket

packetToSend = {
		"seqNo":10000,
		"ackNo":0,
		"syn":False,
		"fin":False,
		"ack":False,
		"rst":False,
		"psh":False,
		"urg":False,
		"data":"Some data"
		}

def resetPacket():

	packetToSend["syn"] = False
	packetToSend["ack"] = False
	packetToSend["fin"] = False
	packetToSend["rst"] = False
	packetToSend["psh"] = False
	packetToSend["urg"] = False

states = ["CLOSED","SYN_SENT","ESTABLISHED","FIN_WAIT_1","TIME_WAIT","FIN_wAIT_2","CLOSING"]

def checkState(packetReceived,currentState):

	print("Current state is : ",currentState)

	if currentState == states[1]:
		if packetReceived["syn"] and packetReceived["ack"]:
			packetToSend["ack"] = True
			packetToSend["seqNo"] = packetReceived["ackNo"]
			packetToSend["ackNo"] = packetReceived["seqNo"] + 1
			currentState = states[2]
			print("State changed to : ",currentState)
			return currentState

	if currentState == states[3]:
		if packetReceived["fin"] and packetReceived["ack"]:
			packetToSend["ack"] = True
			packetToSend["seqNo"] = packetReceived["ackNo"]
			packetToSend["ackNo"] = packetReceived["seqNo"] + 1
			currentState = states[4]
			print("State changed to : ",currentState)
			print("Waits for 2MSL time and state changes to closed!!!")
			return states[0]

	return currentState

def connectToServer():

	host = socket.gethostname()
	port = 9994
	clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSocket.connect((host,port))

	print("Connected to server....")
	packetToSend["syn"] = True
	print("Packet to send : ",packetToSend)
	data = pickle.dumps(packetToSend,-1)
	clientSocket.send(data)
	resetPacket()
	currentState = states[1]
	print("currentState : ",currentState,"\n")

	dataReceived = clientSocket.recv(1024)
	packetReceived = pickle.loads(dataReceived)
	print("Packet Received : ",packetReceived)
	currentState = checkState(packetReceived,currentState)
	data = pickle.dumps(packetToSend,-1)
	clientSocket.send(data)
	print("currentState : ",currentState,"\n")

	dataReceived = clientSocket.recv(1024)

	resetPacket()
	packetToSend["fin"] = True
	data = pickle.dumps(packetToSend,-1)
	currentState = states[3]
	clientSocket.send(data)
	print("currentState : ",currentState,"\n")

	dataReceived = clientSocket.recv(1024)
	packetReceived = pickle.loads(dataReceived)
	print("Packet Received : ",packetReceived)
	currentState = checkState(packetReceived,currentState)
	data = pickle.dumps(packetToSend,-1)
	clientSocket.send(data)
	print("currentState : ",currentState,"\n")

	clientSocket.close()

if __name__ == "__main__":
	connectToServer()
