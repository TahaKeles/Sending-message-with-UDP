import time
import socket
from threading import Thread

# Server
def server(UDP_PORT, N=1000):
    
    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
        print("Socket successfully created")
        
        sock.bind(("", UDP_PORT))

        for i in range(N):
            data, address = sock.recvfrom(1024)
            sock.sendto(data.decode().upper().encode(), address)
    except socket.error as err: 
        print("Socket creation failed with error " + err)
    
    finally:
        sock.close()


thread_1 = Thread(target=server, args=(20210,1000)) # Server for 1 
thread_2 = Thread(target=server, args=(20310,1000)) # Server for 2
thread_3 = Thread(target=server, args=(20410,1000)) # Server for 3

# Start Servers
thread_1.start()
thread_2.start()
thread_3.start()

# Close Threads
thread_1.join()
thread_2.join()
thread_3.join()