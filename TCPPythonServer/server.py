#!/usr/bin/env python3

# first of all import the socket library 
import socket
import sys


#Server functions
def HandleLoginFromClient(userOption):

   f = open('logins.txt', 'r+')

   users = []
   lines = f.readlines()

   for line in lines: 
      users.append(line.rstrip('\n'))

   f.close()
   
   if userOption == "new":

      c.send("requestNewData".encode())
      clientData = c.recv(1024)

      userInfo = clientData.decode()

      temp = userInfo.rstrip("\n")
      newUsername = temp.split(":")

      userNames = []
      temp = []
      for split in users:
         temp = split.split(":")
         userNames.append(temp[0])

      print (userNames)

      if newUsername[0] in userNames:
         return "2" #return username existing
      else:
         file = open('logins.txt', 'a+')
         
         file.write(userInfo)
         file.close()
         return "3" #return new user created
         
   else:
      c.send("requestNewData".encode())
      
      clientData = c.recv(1024)
      info = clientData.decode()
      
      userInfo = info.rstrip("\n")

      if userInfo in users:
         return "1" #return successful
      else:
         return "4" #return user not found
      
# next create a socket object 
s = socket.socket()		 
print ("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345			

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('127.0.0.1', port))		 
print ("socket binded to %s" %(port) )


# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")		

# a forever loop until we interrupt it or 
# an error occurs


filename = "recived.txt"


while True: 
   
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got connection from', addr)

   while True:
      data = c.recv(1024)

      #Client attempt to log in
      if data == b"LOGGIN":
         while True:
            userOption = c.recv(1024)
            userData = userOption.decode()
            outputToClient = HandleLoginFromClient(userData)
            c.send(outputToClient.encode())

            if outputToClient == "1":
               print ("BREAK CALL OUTPUT")
               break
         

   # recive file from client

      elif data == b"PICTURE":

         filename = c.recv(1024)
         filename = filename.decode()
         filename = filename + ".jpg"
         
         filetodown = open(filename,"w+b")
         x = 0
         while x == 0:
            data = c.recv(1024)
            if data == b"DONE":
               print("done reciving")
               x = 1
            filetodown.write(data)
         filetodown.close()
         print ("DEBUGG: END IF PICTURE SEND")

      elif data == b"TEXTFILE":
         filename = c.recv(1024)
         filename = filename.decode()
         filename = filename + ".txt"

         filetodown = open (filename, "w")
         x = 0
         while x == 0:
            data = c.recv(1024)
            data = data.decode()
            print(data)
            if data == "DONE":
               print ("done reciving")
               x = 1
               break
            filetodown.write(data)
         filetodown.close()
         
      else:
         print ("DEBUGG: END OF SERVER CODE")
         c.close()
         break
      
   
