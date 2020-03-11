#!/usr/bin/env python3

import socket,threading
f = open('logins.txt', 'r')
users = {}
lines = f.read().split(':')
users = lines
f.close()
host = "127.0.0.1"
port = 5000
status = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
# uname = raw_input("Enter username: ")
# uname = input("Enter username: ")
# print('Uname: '+ str(uname))
while status != "q":
    status = input("Are you a registered user? y/n? Press q to quit: ")  

    if status == "n": #create new login
         createLogin = input("Create login name: ")

         if createLogin in users: # check if login name exist in the dictionary
             print ("Login name already exist!\n")
         else:
             createPassw = input("Create password: ")
             users[createLogin] = createPassw # add login and password
             print("\nUser created!\n")     

    elif status == "y": #login the user
        login = input("Enter login name: ")

        if login in users:
           passw = input("Enter password: ")
           print

           if login in users and passw in users: # login matches password
               print ("Login successful!\n")
               clientRunning = True
               s.send(login.encode('ascii'))
               status = "q"

        else:
            print
            print("User doesn't exist!\n")

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
   data = login + '>> ' + tempMsg
   s.send(data.encode('ascii'))