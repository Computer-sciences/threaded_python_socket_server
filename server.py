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
#       add server shutdown and restart commands

ascii_format = 'ascii'

all_ascii_connections = []
all_ascii_aliases = []

def broadcast(broadcast_group, message):
    for connection in broadcast_group:
        try:
            connection.send(message)
        except:
            continue

def remove_ascii_connection(connection):
    index = all_ascii_connections.index(connection)
    alias = all_ascii_aliases[index]
    broadcast(all_ascii_connections, "~ connection ~ {} is no longer connected.\n".format(alias).encode(ascii_format))
    all_ascii_connections.remove(connection)
    all_ascii_aliases.remove(alias)
    connection.close()

def close_all_connections():
    for connection in all_ascii_connections:
        connection.close()
    all_ascii_connections[:]
    all_ascii_aliases[:]

################
# Instruction headers:

close_instruction = 'close'.encode(ascii_format)
server_stats_instruction = 'how many'.encode(ascii_format)

################

def an_individual_ascii_connection(connection, connection_address):
    index = all_ascii_connections.index(connection)
    alias = all_ascii_aliases[index].encode(ascii_format)
    connected = True
    while connected:
        try:
            message = connection.recv(1024)
            broadcast_message = alias + b": " + message + b"\n"
            print("{} said: {}".format(connection_address, message))
            print("{} was sent as a full broadcast\n".format(broadcast_message))
            broadcast(all_ascii_connections, broadcast_message)
            if message == close_instruction:
                user_goodbye = "~ external ~ {} closed their connection.\n".format(alias).encode(ascii_format)
                print(user_goodbye)
                broadcast(all_ascii_connections, user_goodbye)
                connected = False
            if message == server_stats_instruction:
                connection.send("~ count ~ There is/are {} active connection/s.\n".format(threading.activeCount() - 1).encode(ascii_format))
        except:
            connected = False
    remove_ascii_connection(connection)




ip_server = socket.gethostbyname(socket.gethostname())
port_server = 10000

ascii_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ascii_server.bind((ip_server, port_server))




def start_routing():

    ascii_server.listen(16)
    print("\n~ listen ~ The ascii server is listening on {}:{}\n".format(ip_server, port_server))

    close_all_connections()

    while True:
        ascii_client, ascii_client_address = ascii_server.accept()
        print("A computer successfully connected from {}.".format(str(ascii_client_address)))

        ascii_client.send('send_an_alias'.encode(ascii_format))
        alias = ascii_client.recv(1024).decode(ascii_format)

        print("New connection alias is {}\n".format(alias))
        all_ascii_aliases.append(alias)
        all_ascii_connections.append(ascii_client)

        broadcast(all_ascii_connections, "{} joined the chat.\n".format(alias).encode(ascii_format))
        ascii_client.send('You have successfully connected.\n'.encode(ascii_format))

        # Add address to args
        ascii_thread = threading.Thread(target=an_individual_ascii_connection, args=(ascii_client, ascii_client_address))
        ascii_thread.start()




#
start_routing()