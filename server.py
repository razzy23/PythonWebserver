from email.mime import image
from inspect import modulesbyfile
from multiprocessing.connection import Client
from operator import methodcaller
import socket
#since the server uses socket module, import the socket module

HOST, PORT = '', 2728 #assigning the host IP and the port

sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#create new socket object as "sock", AF_INET is the socket family (IPv4) in this case
#SOCK_STREAM is the socket type, which is connection oriented, uses TCP

sockt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockt.bind((HOST, PORT)) #giving the host address and the port to the socket created
sockt.listen(1)
print('Serving HTTP on port',PORT, '...')

while True:
    conn, addr = sockt.accept()
    req = conn.recv(1024).decode('utf-8')# returns the request details of 1024B from the connection.
    print(req) #prints the request, decoded with utf-8

    stringlist = req.split(" ") #split the request return at the spaces
    method = stringlist[0] #first string of the splitted request is a method
    reqfile = stringlist[1] #the request file

    print("Clinet request", reqfile)

    myfile = reqfile.split('?')[0] #removing the data from the file name
    myfile = myfile.lstrip('/')

    if (myfile == ''):
        myfile = 'index.html' #load index file as default

    try:
        file = open(myfile, 'rb') #open the file
        res = file.read()
        file.close() #stores the data in the file into 'res' and closes it

        header = 'HTTP/1.1 200 OK\n'

        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = "text/html"
        
        header += 'Content-Type: '+str(mimetype)+'\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        res = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
    final_res = header.encode('utf-8')
    final_res += res
    conn.send(final_res)
    conn.close() #closes the connection