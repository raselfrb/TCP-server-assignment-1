import socket, threading
host = "127.0.0.1"
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
clients = {}
print("Server is ready...")
serverRunning = True
def handle_client(conn, login):

    clientConnected = True
    keys = clients.keys()
    help = 'There are 3 commands so far.\n1**list > gives you the list of the people currently online\n2**quit > To end your session and quit the server\n3**(username) sends a private message to any user you want'

    while clientConnected:
        try:
            response = 'Number of People Online\n'
            data = conn.recv(1024).decode('ascii')
            found = False
            if '**' not in data:
                for k,v in clients.items():
                    if v != conn:
                        v.send(data.encode('ascii'))
                        found = True


            elif '**list' in data:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) +'::' + name+'\n'
                conn.send(response.encode('ascii'))
                found = True


            elif '**help' in data:
                conn.send(help.encode('ascii'))
                found = True
            else:
                for name in list(clients):
                    if('**'+name) in data:
                        data = data.replace('**'+name,'')
                        clients.get(name).send(data.encode('ascii'))
                        found = True
                    if('**kick '+name) in data:
                        print('Name: '+ name)
                        print('Client: '+ str(clients))
                        # clients.pop(name)
                        del clients[name]
                        found = True
                if(not found):
                    conn.send('Trying to send message to invalid person.'.encode('ascii'))


        except:
            print(login + ' has logged out')
            clientConnected = False

while serverRunning:
    conn,addr = s.accept()
    login = conn.recv(1024).decode('ascii')
    print('User : '+ login)
    print('%s connected to the server'%str(login))
    conn.send('Welcome to the Server. Type **help to know all the commands'.encode('ascii'))

    if(conn not in clients):
        print("Conn: " + str(conn))
        clients[login] = conn
        threading.Thread(target = handle_client, args = (conn, login,)).start()