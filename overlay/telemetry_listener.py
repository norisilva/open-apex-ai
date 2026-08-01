import socket
import ctypes
import threading

class PacketHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', ctypes.c_uint16),
        ('m_gameYear', ctypes.c_uint8),
        ('m_gameMajorVersion', ctypes.c_uint8),
        ('m_gameMinorVersion', ctypes.c_uint8),
        ('m_packetVersion', ctypes.c_uint8),
        ('m_packetId', ctypes.c_uint8),
        ('m_sessionUID', ctypes.c_uint64),
        ('m_sessionTime', ctypes.c_float),
        ('m_frameIdentifier', ctypes.c_uint32),
        ('m_overallFrameIdentifier', ctypes.c_uint32),
        ('m_playerCarIndex', ctypes.c_uint8),
        ('m_secondaryPlayerCarIndex', ctypes.c_uint8)
    ]

class PacketSessionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_weather', ctypes.c_uint8),
        ('m_trackTemperature', ctypes.c_int8),
        ('m_airTemperature', ctypes.c_int8),
        ('m_totalLaps', ctypes.c_uint8),
        ('m_trackLength', ctypes.c_uint16),
        ('m_sessionType', ctypes.c_uint8),
        ('m_trackId', ctypes.c_int8),
    ]

class TelemetryListener(threading.Thread):
    def __init__(self, port, callback, status_callback=None):
        super().__init__()
        self.port = port
        self.callback = callback
        self.status_callback = status_callback
        self.running = False
        self.sock = None
        self.daemon = True
        self.last_track_id = -1
        
    def stop(self):
        self.running = False
        if self.sock:
            try:
                # Dummy packet to unblock recvfrom
                dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dummy_sock.sendto(b'', ('127.0.0.1', self.port))
                dummy_sock.close()
            except:
                pass
            
    def run(self):
        self.running = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Permite compartilhar a porta com outros aplicativos de telemetria
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', self.port))
            # 1 second timeout to periodically check if we should stop
            self.sock.settimeout(1.0)
            
            if self.status_callback:
                self.status_callback(f"Ouvindo porta {self.port}", "green")
                
            print(f"Servidor UDP iniciado na porta {self.port}")
            
            while self.running:
                try:
                    data, addr = self.sock.recvfrom(2048)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Erro no socket: {e}")
                    break
                    
                if not data:
                    continue
                    
                # The header is 29 bytes
                if len(data) < 29:
                    continue
                    
                header = PacketHeader.from_buffer_copy(data[:29])
                
                # m_packetId == 1 means it's a Session Packet
                if header.m_packetId == 1 and len(data) >= ctypes.sizeof(PacketSessionData):
                    session_packet = PacketSessionData.from_buffer_copy(data)
                    track_id = session_packet.m_trackId
                    
                    if track_id != self.last_track_id and track_id >= 0:
                        self.last_track_id = track_id
                        print(f"Telemetria detectou pista ID: {track_id}")
                        if self.callback:
                            self.callback(track_id)
                            
        except Exception as e:
            print(f"Erro ao iniciar servidor UDP: {e}")
            if self.status_callback:
                self.status_callback(f"Erro porta {self.port}", "red")
        finally:
            if self.sock:
                self.sock.close()
