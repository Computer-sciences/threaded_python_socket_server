import socket
import threading

# Change this to only show if asked

chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chatter.connect(('127.0.0.1', 10000))
ttl = 16

def receive():
    attempts = 0
    while True:
        try:
            message = chatter.recv(1024).decode('ascii')
            if message == 'send_an_alias':
                alias = input("Enter your alias: ")
                chatter.send(alias.encode('ascii'))
                print("")
                write_thread.start()
            else:
                attempts += 1
                print(message)
                if attempts == ttl:
                    chatter.close()
                    print("The connection was lost. Press enter to exit.")
                    break
        except:
            chatter.close()
            print("The connection was closed. Press enter to exit")
            break

def write():
    while chatter:
            message = f'{input("")}'
            if (chatter):
                try:
                    chatter.send(message.encode('ascii'))
                except:
                    print("Exiting due to no connection.")
                    break

    chatter.close()
    print("The connection was closed.")


# start both threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)