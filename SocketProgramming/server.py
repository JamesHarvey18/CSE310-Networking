import socket

port = int(input("Choose a port\n"))  # Prompts user to enter port number
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # establishes the socket as TCP connection
serverSocket.bind(('', port))  # Binds the socket to localhost for IP address, port number given by user
serverSocket.listen(1)  # Has socket listen to only 1 connection at a time
print('Server is ready for requests\n')

dictionary = {}  # Dictionary to store key value pairs on server


# All methods for valid requests given to server
def get(key):
    if key in dictionary.keys():
        response = "HTTP /1.1 200 OK\n" + dictionary.get(key)
        client.send(response.encode("utf-8"))
    else:
        client.send("HTTP /1.1 404 NOT FOUND".encode("utf-8"))


def put(key, value):
    dictionary[key] = value
    client.send("HTTP /1.1 200 OK".encode("utf-8"))


def delete(key):
    dictionary.pop(key)
    client.send("HTTP /1.1 200 OK".encode("utf-8"))


def clear():
    dictionary.clear()
    client.send("HTTP /1.1 200 OK".encode("utf-8"))


def quit():
    client.send("HTTP /1.1 200 OK")
    client.close()
    dictionary.clear()


while True:  # Leaves server constantly running
    client, ca = serverSocket.accept()  # accepts new connection

    while True:  # secondary loop to prevent server from getting hung up on accepting a new connection
        request = client.recv(1024)  # Receive the message from the client

        args = request.split()  # splits message into a list
        req = args[0]

        if len(args) == 2:  # checks length of list to decide what variables it needs to set
            key = args[1]
        elif len(args) == 3:
            key = args[1]
            value = args[2]

        if req == 'GET':  # selector statements for each possible request
            if len(args) == 2:
                get(key)
            else:
                client.send("HTTP /1.1 400 BAD REQUEST")
        elif req == 'PUT':
            if len(args) == 3:
                put(key, value)
            else:
                client.send("HTTP /1.1 400 BAD REQUEST")
        elif req == 'DELETE':
            if len(args) == 2:
                delete(key)
            else:
                client.send("HTTP /1.1 400 BAD REQUEST")
        elif req == 'CLEAR':
            if len(args) == 1:
                clear()
            else:
                client.send("HTTP /1.1 400 BAD REQUEST")
        elif req == 'QUIT':
            if len(args) == 1:
                quit()
                break
            else:
                client.send("HTTP /1.1 400 BAD REQUEST")
        else:  # if no valid request is given, unsupported code is sent in response
            client.send("HTTP /1.1 220 UNSUPPORTED")

        args = []  # resets list of arguments
