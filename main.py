import socket
from time import sleep
"""
server_ip = str(input("Enter IRC server domain: "))
port = int(input("Enter IRC server port (default 6667): ") or 6667)
nickname = str(input("Enter your nickname: "))
#password = str(input("Enter your password: "))
"""

# irc.hackclub.com
# chat.freenode.net
# localhost

server_ip = "localhost"
port = 6667
nickname = "spessman"

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
#print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)

# Send USER command
s.send(b"USER zIRClient 0 * :zIRConium\n")
sleep(1)

Ping = s.recv(1024).decode("utf-8")
print(Ping)  # Debug response
#if "PING" in Ping:
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

while True:

    input_msg = input(f"{nickname} [foul_tarnished]: ")

    #channel = "Commands"

    first_char = input_msg[0]
    
    if first_char == "/":
        command = input_msg[1:].split()[0].upper()
        """
        channel = input_msg.split()[1]
        print(f"JOIN {channel}")
        """
        if command == "JOIN":
            channel = input_msg.split()[1]
            print(f"JOIN {channel}")
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
        s.send(f"PRIVMSG #lounge :{input_msg}\n".encode("utf-8")) # type: ignore
    
    while True:
        response = s.recv(1024).decode("utf-8")
        print(response)  # Debug response
        if "PING" in response:
            server_ping = response.split()[1]
            #print(f"Responding to server PING with: {server_ping}")
            s.send(f"PONG {server_ping}\n".encode("utf-8"))
        else:
            break

# Keep the connection open
# while True:
# print(s.recv(1024).decode("utf-8"))
