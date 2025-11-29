import socket
from time import sleep
import threading
import queue

server_ip = str(input("Enter IRC server domain: "))
port = int(input("Enter IRC server port (default 6667): ") or 6667)
nickname = str(input("Enter your nickname: "))
#password = str(input("Enter your password: "))

# irc.hackclub.com
# chat.freenode.net
# localhost
"""
server_ip = "irc.hackclub.com"
port = 6667
nickname = "spessman"
"""
channel = "Commands"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, port))

#print("!1")
#stuff = s.recv(1024).decode("utf-8")
#print(stuff)  # Debug response

# Send PASS command
"""
s.send(f"PASS {password}\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""

#print("!2")

# Send NICK command
s.send(f"NICK {nickname}\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)

# Send USER command
s.send(b"USER zIRClient 0 * :zIRConium\n")
sleep(1)

Ping = s.recv(1024).decode("utf-8")
print(Ping)  # Debug response
if "PING" in Ping:
    server_ping = Ping.split()[1]
    print(f"Responding to server PING with: {server_ping}")
    s.send(f"PONG {server_ping}\r\n".encode("utf-8"))
#print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)

"""
# Register with NickServ
s.send(b"MSG NickServ :REGISTER YourPassword your@email.com\n")
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""
# s.send(b"MSG NickServ REGISTER YourPassword your@email.com\n")

# Authenticate with NickServ
"""
s.send(b"PRIVMSG NickServ :IDENTIFY sgrumblo\n")
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""
# Join a channel
#s.send(b"JOIN #irs-ysws\n")
#print(s.recv(1024).decode("utf-8"))  # Debug response

# Set the socket to non-blocking mode
s.setblocking(False)

# Create a queue for non-blocking input
input_queue = queue.Queue()

def get_input(input_queue):
    while True:
        user_input = input(f"{nickname} [{channel}]: ")
        input_queue.put(user_input)

# Start the input thread
input_thread = threading.Thread(target=get_input, args=(input_queue,), daemon=True)
input_thread.start()

while True:
    # Check if there's input in the queue
    if not input_queue.empty():
        input_msg = input_queue.get()

        first_char = input_msg[0]
        
        if first_char == "/":
            command = input_msg[1:].split()[0].upper()
            if command == "JOIN":
                channel = input_msg.split()[1]
                print(f"JOIN {channel}")
                s.send(f"JOIN 0\n".encode("utf-8"))
                s.send(f"JOIN {channel}\n".encode("utf-8"))
            elif command == "PART":
                channel = input_msg.split()[1]
                s.send(f"PART {channel}\n".encode("utf-8"))
            elif command == "LIST":
                s.send(b"LIST\n")
            elif command == "QUIT":
                s.send(b"QUIT\n")
                break
            else:
                print("Unknown command.")
        else:
            s.send(f"PRIVMSG {channel} :{input_msg}\n".encode("utf-8")) # type: ignore

    # Process server responses
    try:
        response = s.recv(1024).decode("utf-8")
        print(f"\n{response}")  # Print server response on a new line
        if "PING" in response:
            server_ping = response.split()[1]
            s.send(f"PONG {server_ping}\n".encode("utf-8"))
        
        # Reprint the input prompt
        print(f"{nickname} [{channel}]: ", end="", flush=True)
    except BlockingIOError:
        # No data received, continue the loop
        pass
    except socket.error as e:
        print(f"Socket error: {e}")
        break

# Keep the connection open
# while True:
# print(s.recv(1024).decode("utf-8"))
