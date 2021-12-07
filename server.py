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
    broadcast(all_connections, f"~ lost connection ~ An error occurred for {alias}. They are no longer connected.".encode(data_format))
    all_connections.remove(connection)
    all_aliases.remove(alias)
    connection.close()

def close_all_connections():
    for connection in all_connections:
        connection.close()
    all_connections.clear()
    all_aliases.clear()

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
            broadcast_message = alias + b": " + message
            print(f"{connection_address} said: {message}")
            print(f"{broadcast_message} was sent as a full broadcast")
            broadcast(all_connections, broadcast_message)
            if message == close_instruction:
                user_goodbye = f"~ external ~ {alias} closed their connection.".encode(data_format)
                print(user_goodbye)
                broadcast(user_goodbye)
                connected = False
            if message == server_stats_instruction:
                connection.send(f"~ count ~ There is/are {threading.activeCount() - 1} active connection/s.".encode(data_format))
        except:
            connected = False
    remove_connection(connection)




ip_server = socket.gethostbyname(socket.gethostname())
port_server = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_server, port_server))
server.listen()
print(f"~ listen ~ The server is listening on {ip_server}:{port_server}")




def start_routing():
    while True:
        client, address = server.accept()
        print(f"A computer successfully connected from {str(address)}.")

        client.send('send_an_alias'.encode(data_format))
        alias = client.recv(1024).decode(data_format)

        print(f"New connection alias is {alias}")
        all_aliases.append(alias)
        all_connections.append(client)

        broadcast(all_connections, f'{alias} joined the chat.'.encode(data_format))
        client.send('You have successfully connected.'.encode(data_format))

        # Add address to args
        thread = threading.Thread(target=an_individual_connection, args=(client, address))
        thread.start()

close_all_connections()
start_routing()