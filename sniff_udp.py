import socket
import struct
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))
sock.settimeout(3.0)

try:
    print("Sniffing...")
    start = time.time()
    packets = []
    while time.time() - start < 1.0:
        data, addr = sock.recvfrom(2048)
        if len(data) >= 29:
            pf, _, _, _, _, pid, _, _, _, _, _, _ = struct.unpack('<HBBBBBQfIIBB', data[:29])
            packets.append((pf, pid, len(data)))
            
    print("Found packets:", set(packets))
except Exception as e:
    print("Error:", e)
finally:
    sock.close()
