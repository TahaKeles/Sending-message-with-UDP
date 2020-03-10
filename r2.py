import time, random
import socket
from threading import Thread

# Client
def client(UDP_IP ,UDP_PORT, N=1000, output=[]):

    # Create a datagram socket
    # Notice the use of SOCK_DGRAM for UDP packets
    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
        print("Socket successfully created")

        delaySum = 0 

        # Send message to IP Port pair
        for i in range(N):
            start = time.time()
            sock.sendto("MESSAGE".encode(), (UDP_IP, UDP_PORT)) ## TO SEND
            data, address = sock.recvfrom(1024)
            delaySum = delaySum + (time.time() - start)   

    except socket.error as err: 
        print("Socket creation failed with error " + err)

    finally:
        sock.close()
        avgDelay = delaySum/1000
        print(avgDelay)
        output.append(avgDelay)

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


thread_1 = Thread(target=server, args=(20230,1000)) # Server for 1
thread_3 = Thread(target=server, args=(20430,1000)) # Server for 3

retVal_S = []
retVal_D = []
thread_s = Thread(target=client, args=("10.10.2.2", 20310, 1000, retVal_S)) # Client for S 
thread_d = Thread(target=client, args=("10.10.5.2", 20350, 1000, retVal_D)) # Client for D

# First Start Servers
thread_1.start()
thread_3.start()

# Then Start Clients
thread_s.start()
thread_d.start()

# Close Threads
thread_s.join()
thread_d.join()

print("R2 - S, ",  retVal_S[0])
print("R2 - D, ",  retVal_D[0])

file = open("link_cost.txt","w+")
file.write("Link Cost of R2 - S is "  + str(retVal_S[0]) + "\r\n")
file.write("Link Cost of R1 - D is "  + str(retVal_D[0]) + "\r\n")
file.close()
print("link_cost.txt created.")