import threading
import socket

# todo: headers for server socket as import (classed data)
#       function to print strings at equal start points
#       make instruction  "How many?"
#       allow clients to close the connection with a message
#       swap ip with alias for the broadcast
#       create class files
#       add a sys.stdout log file
#       add a ttyl for failed attempts
#       add data cleansing methods
#       handle threads
#       add a server restart method

data_format = 'ascii'

all_connections = []
all_aliases = []

def broadcast(broadcast_group, message):
    for connection in broadcast_group:
        try:
            connection.send(message)
        except:
            continue

def remove_connection(connection):
    index = all_connections.index(connection)
    alias = all_aliases[index]
    broadcast(all_connections, "~ connection ~ {} is no longer connected.\n".format(alias).encode(data_format))
    all_connections.remove(connection)
    all_aliases.remove(alias)
    connection.close()

def close_all_connections():
    for connection in all_connections:
        connection.close()
    all_connections[:]
    all_aliases[:]

################
# Instruction headers:

close_instruction = 'close'.encode(data_format)
server_stats_instruction = 'how many'.encode(data_format)

################

def an_individual_connection(connection, connection_address):
    index = all_connections.index(connection)
    alias = all_aliases[index].encode(data_format)
    connected = True
    while connected:
        try:
            message = connection.recv(1024)
            broadcast_message = alias + b": " + message + b"\n"
            print("\n{} said: {}".format(connection_address, message))
            print("{} was sent as a full broadcast".format(broadcast_message))
            broadcast(all_connections, broadcast_message)
            if message == close_instruction:
                user_goodbye = "~ external ~ {} closed their connection.\n".format(alias).encode(data_format)
                print(user_goodbye)
                broadcast(all_connections, user_goodbye)
                connected = False
            if message == server_stats_instruction:
                connection.send("~ count ~ There is/are {} active connection/s.\n".format(threading.activeCount() - 1).encode(data_format))
        except:
            connected = False
    remove_connection(connection)




ip_server = socket.gethostbyname(socket.gethostname())
port_server = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_server, port_server))
server.listen(256)
print("~ listen ~ The server is listening on {}:{}".format(ip_server, port_server))




def start_routing():
    while True:
        client, address = server.accept()
        print("A computer successfully connected from {}.".format(str(address)))

        client.send('send_an_alias'.encode(data_format))
        alias = client.recv(1024).decode(data_format)

        print("New connection alias is {}".format(alias))
        all_aliases.append(alias)
        all_connections.append(client)

        broadcast(all_connections, "{} joined the chat.\n".format(alias).encode(data_format))
        client.send('You have successfully connected.\n'.encode(data_format))

        # Add address to args
        thread = threading.Thread(target=an_individual_connection, args=(client, address))
        thread.start()

close_all_connections()
start_routing()