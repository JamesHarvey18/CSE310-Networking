import os
import struct
import socket
import time
import statistics

def checksum(data):
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return struct.pack('<H', ~x & 0xFFFF)

def ping(dest_addr, timeout, tries, data=b''):
    icmp = socket.getprotobyname("icmp")
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    ICMP_TYPE = 8  # Indicates an echo request
    ICMP_CODE = 0  # Indicates a ping reply
    ID = os.getpid() & 0xFFFF  # The ID will be set the ID of your running program. Since we are only given so much space, we only use the first 2 bytes
    SEQUENCE = 1  # You don't have to continuously communicate with the server. By setting the SEQ number to 1, we can treat all attempts as separate.
    CHECKSUM = 0
    header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE) + data

    while tries > 0:
        try:
            sock.connect((dest_addr, 80))
            sock.sendall(b'\x08\0' + checksum(b'\x08\0\0\0' + header) + header)
            startTime = time.time()
            sock.settimeout(timeout)
            data = sock.recv(1024)
            if data[20:] == b'\0\0' + checksum(b'\0\0\0\0' + header) + header:
               return time.time() - startTime

        except socket.gaierror:
            print("Address incorrect")

        tries = tries - 1

    if tries == 0:
        print("Packet not received")

if __name__ == '__main__':
    googlePing = ping('google.com', 2, 4) * 1000
    youtubePing = ping('youtube.com', 2, 4) * 1000
    facebookPing = ping('facebook.com', 2, 4) * 1000
    redditPing = ping('reddit.com', 2, 4) * 1000

    print("\nGoogle's ping: " + str(googlePing) + " ms")
    print("YouTube's ping: " + str(youtubePing) + " ms")
    print("Facebook's ping: " + str(facebookPing) + " ms")
    print("Reddit's ping: " + str(redditPing) + " ms")

    statSummary = {'Google': googlePing, 'Youtube': youtubePing, 'Facebook': facebookPing, 'Reddit': redditPing}
    stats = [googlePing, youtubePing, facebookPing, redditPing]

    minimumPing = min(statSummary, key=statSummary.get)
    print("\nMinimum ping is from " + minimumPing + ": " + str(statSummary[minimumPing]) + " ms")
    maximumPing = max(statSummary, key=statSummary.get)
    print("Maximum ping is from " + maximumPing + ": " + str(statSummary[maximumPing]) + " ms")
    averagePing = (googlePing + youtubePing + facebookPing + redditPing) / 4
    print("Mean ping is: " + str(averagePing))
    standardDeviation = statistics.stdev(stats)
    print("Standard Deviation of ping is: " + str(standardDeviation) + " ms")