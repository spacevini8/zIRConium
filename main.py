import socket
from time import sleep
"""
server_ip = str(input("Enter IRC server domain: "))
port = int(input("Enter IRC server port (default 6667): ") or 6667)
nickname = str(input("Enter your nickname: "))
#password = str(input("Enter your password: "))
"""

server_ip = "irc.hackclub.com"
port = 6667
nickname = "spessman"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, port))

print(s.recv(1024).decode("utf-8"))  # Debug response

# Send PASS command
"""
s.send(f"PASS {password}\r\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""
# Send NICK command
s.send(f"NICK {nickname}\r\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)

# Send USER command
s.send(b"USER guest 0 * :Hugh Mann\r\n")
sleep(1)
Ping = s.recv(1024).decode("utf-8")
print(Ping)  # Debug response
#if "PING" in Ping:
server_ping = Ping.split()[1]
print(f"Responding to server PING with: {server_ping}")
s.send(f"PONG {server_ping}\r\n".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)



"""
# Register with NickServ
s.send(b"MSG NickServ :REGISTER YourPassword your@email.com\r\n")
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""
# s.send(b"MSG NickServ REGISTER YourPassword your@email.com\r\n")

# Authenticate with NickServ
"""
s.send(b"PRIVMSG NickServ :IDENTIFY sgrumblo\r\n")
print(s.recv(1024).decode("utf-8"))  # Debug response
sleep(1)
"""
# Join a channel
#s.send(b"JOIN #irs-ysws\r\n")
#print(s.recv(1024).decode("utf-8"))  # Debug response

while True:

    response = s.recv(1024).decode("utf-8")
    print(response)  # Debug response
    if "PING" in response:
        server_ping = response.split()[1]
        #print(f"Responding to server PING with: {server_ping}")
        s.send(f"PONG {server_ping}\r\n".encode("utf-8"))
    
    input_msg = input(f"{nickname}: ")
    
    first_char = input_msg[0]
    
    if first_char == "/":
        command = input_msg[1:].split()[0].upper()
        if command == "join":
            channel = input_msg.split()[1]
            s.send(f"JOIN {channel}\r\n".encode("utf-8"))
        elif command == "part":
            channel = input_msg.split()[1]
            s.send(f"PART {channel}\r\n".encode("utf-8"))
        elif command == "list":
            s.send(b"LIST\r\n")
        elif command == "quit":
            s.send(b"QUIT\r\n")
            break
        else:
            print("Unknown command.")
    else:
        s.send(f"PRIVMSG {channel} : {input_msg}\r\b".encode("utf-8")) # type: ignore

# Keep the connection open
# while True:
# print(s.recv(1024).decode("utf-8"))
