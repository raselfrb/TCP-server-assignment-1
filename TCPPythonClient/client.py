#!/usr/bin/env python3

from tkinter import filedialog
from tkinter import *

import os

# Import socket module 
import socket




#Client functions
def SendDataToServer(data):
    s.send(data.encode())

def UserLogin():
    while True:
        status = input ("Are you a registed user? y/n? Press q to close client: ")

        if status == "n": # create a new login
            print ("Register new user!")
            newUsername = input ("Wrtie username: ")
            newPass = input ("Write password: ")
            newUser = newUsername + ":" + newPass + "\n"
            return newUser, "new"
            break

        elif status == "y": #Request user details
            username = input ("Write username: ")
            password = input ("Write password: ")
            userData = username + ":" + password
            return userData, "old"
            break
        
        elif status == "q": #Go out of user menu
            return status, None
            break

        else:
            print ("No valid input!")

filename = "send.txt"


# Create a socket object 
s = socket.socket()		 

# Define the port on which you want to connect 
port = 12345				

# connect to the server on local computer 
s.connect(('127.0.0.1', port))

#Creating client

while True:

    x = True
    flag = True
    loginInfo, userOption = UserLogin()

    s.send(b"LOGGIN")
    
    while x == True:
        if loginInfo == "q":
            print("Closing client!")
            break
        elif flag == True:
            SendDataToServer(userOption)

            #Recive answer from server with result
            serverAnswer = s.recv(1024)

            decodedData = serverAnswer.decode()

            if decodedData == "requestNewData":
                SendDataToServer(loginInfo)
                x = True
                flag = False

        else:

            serverAnswer = s.recv(1024)

            decodedData = serverAnswer.decode()
            
            if decodedData == "1": #sucessful login
                
                print ("Sucessfully logged into server!")
                while True:
                    print ("\n")
                    print ("What would you like to do?")
                    print ("1 - Send .jpg file to server")
                    print ("2 - Exit and close client")

                    optionInput = input("Write your choice: ")

                    

                    if optionInput == "1":

                        root = Tk()
                        root.filename =  filedialog.askopenfilename(initialdir = "/",
                                                                    title = "Select file",
                                                                    filetypes = (("jpeg files","*.jpg"),("txt file", "*.txt")))

                        path, exten = os.path.splitext(root.filename)

                        
                        if exten == ".jpg":
                            s.send(b"PICTURE")

                            serverFileName = input ("Save the file as: ")

                            s.send(serverFileName.encode())

                            filetosend = open(root.filename, "r+b")
                            data = filetosend.read(1024)
                            while data:
                                print("sending...")
                                s.send(data)
                                data = filetosend.read(1024)
                            filetosend.close()
                            s.send(b"DONE")
                            print("Done sending")
    
                        elif exten == ".txt":
                            s.send(b"TEXTFILE")

                            serverFileName = input ("Save the file as: ")

                            s.send(serverFileName.encode())

                            filetosend = open(root.filename, "r")

                            data = filetosend.read(1024)
                            while data:
                                print("sending...")
                                s.send(data.encode())
                                data = filetosend.read(1024)
                            filetosend.close()
                            s.send(b"DONE")
                            print("Done sending")

                        else:
                            print("Not a valid file!")
                            

                        
                            
                    elif optionInput == "2":
                        
                        break
                    else:
                        print ("No valid input!")

                break
                
            elif decodedData == "2": #username is already in use
                print ("Username already exist!")
                break

            elif decodedData == "3":
                print ("User created!")
                break
            
            else: #username does not exist
                print ("User does not exist!")
                break
            
    break

s.close()    
