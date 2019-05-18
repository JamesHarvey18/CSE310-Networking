import socket
import time

host=input("Target host (localhost for your own machine): ")
port=int(input("Target port: "))

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost",port))

while True:
	cmd=input("")
	split=cmd.split()
	if split[0].lower() is not "quit":
		sock.send(cmd.encode("utf-8"))
		print(sock.recv(1024).decode())
	else:
		sock.close()