import socket
import threading

# Change this to only show if asked

chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chatter.connect(('192.168.56.1', 10000))

accepting_messages = True

def receive():
    while accepting_messages:
        try:
            message = chatter.recv(1024).decode('ascii')
            if message == 'send_an_alias':
                alias = input("Enter your alias: ")
                chatter.send(alias.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print("The connection was closed.")
            chatter.close()
            break

def write():
    message = "open"
    while message != "close":
        message = f'{input("")}'
        chatter.send(message.encode('ascii'))
    accepting_messages = False
    chatter.close()


# start both threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()