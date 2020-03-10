#!/usr/bin/env python3

import socket,threading
host = "127.0.0.1"
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
# uname = raw_input("Enter username: ")
uname = input("Enter username: ")
print('Uname: '+ str(uname))
s.send(uname.encode('ascii'))
clientRunning = True

def echo_data(sock):
   serverDown = False
   while clientRunning and (not serverDown):
      try:
         data = sock.recv(1024).decode('ascii')
         print(data)
      except:
         print('Server is Down. You are now Disconnected. Press enter to exit...')
         serverDown = True


threading.Thread(target=echo_data, args = (s,)).start()
while clientRunning:
   tempMsg = input()
   data = uname + '>> ' + tempMsg
   s.send(data.encode('ascii'))