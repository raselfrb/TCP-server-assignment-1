# TCP Server for user database

# Import modules
from threading import Thread
from datetime import datetime
import socket

# Global variables
host = "127.0.0.1" # Host
port = 50000                                         # Port
addr = (host, port)                               # Tuple address
form_addr = host + ":" + str(port)                # Formatted Address
buff = 2048                                       # Buffer rate

connections = {}
users = {}

# Function to validate forms - Have not used it yet
def validate(form_names, forms, min_len=0, max_len=250):
    """Validates forms are valid lengths and username exists"""

    for form, form_names in zip(forms, form_names):
        if not min_len <= form <= max_len:
            return False
            if form_name == "username" and form not in users:
                return False
    return True

# User class to store individual data for users
class User():
    def __init__(self, password, group, join_date):
        self.password = password
        self.group = group
        self.join_date = join_date


# Threaded connections - Gives each connection its own thread
class Connection(Thread):
    def __init__(self, conn, conn_addr):
        Thread.__init__(self)
        self.conn = conn                     # Connection object
        self.conn_addr = conn_addr           # Connection address (string)

    def send(self, message):                 # Sends data to the client
        try:
            self.conn.send(message.encode())
        except UnicodeEncodeError as e:
            print(str(e))

    def recieve(self, form_name=""):         # Recieves data from the client
        self.send(form_name + " -> ")
        try:
            return self.conn.recv(buff).decode()
        except UnicodeDecodeError:
            self.send("Type exit exit")

    def register(self):
        username = self.recieve(form_name="New Username")
        password = self.recieve(form_name="New Password")

        # Assign new user to object
        users[username] = \
        User(password, "Member",
             datetime.now().strftime("%m/%d/%Y"))

    def login(self):
        username = self.recieve(form_name="Username")
        password = self.recieve(form_name="Password")

        # Perform check
        if username in users:
            if users[username].password == password:
                self.send("Successful login")  # Haven't figured out what to do here yet

    def run(self):
        self.send("Welcome to the server\n")   # Runs when the thread initializes
        while True:
            command = self.recieve().split()
            if not command:  # Checks for user connection loss
                break

# Create socket instance
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to local ip/port
print("\nStarting server on " + form_addr)
try:
    sock.bind(addr)
except socket.error as e:  # Check for port binding error
    print(str(e))

# Listen and accept incoming connections
sock.listen(3)

def listener():
    conn, conn_addr = sock.accept()     # Waits for incoming connection
    conn_addr = conn_addr[0] + ":" + \
                str(conn_addr[1])

    print("Connection from client: " + conn_addr + "\n")

    connections[conn_addr] = Connection(conn, conn_addr) # Initiates connection thread
    connections[conn_addr].start() # Starts run sequence
    # After here the listener goes back to wait for multiple connections

Thread(target=listener).start()

while True:
    command = input("Server command: ")  # Nothing here yet, work in progress
