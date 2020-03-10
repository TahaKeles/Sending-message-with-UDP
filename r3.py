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

retVal_S = []
retVal_2 = []
retVal_D = []

thread_s = Thread(target=client, args=("10.10.3.1", 20410, 1000, retVal_S)) # Client for S 
thread_2 = Thread(target=client, args=("10.10.6.1", 20430, 1000, retVal_2)) # Client for 2
thread_d = Thread(target=client, args=("10.10.7.1", 20450, 1000, retVal_D)) # Client for D

# Start Clients
thread_s.start()
thread_2.start()
thread_d.start()

# Close Threads
thread_s.join()
thread_2.join()
thread_d.join()

print("R3 - S, ",  retVal_S[0])
print("R3 - R2,",  retVal_2[0])
print("R3 - D, ",  retVal_D[0])

file = open("link_cost.txt","w+")
file.write("Link Cost of R3 - S is "  + str(retVal_S[0]) + "\r\n")
file.write("Link Cost of R3 - R2 is " + str(retVal_2[0]) + "\r\n")
file.write("Link Cost of R3 - D is "  + str(retVal_D[0]) + "\r\n")
file.close()
print("link_cost.txt created.")