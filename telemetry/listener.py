import socket
import threading
from telemetry.parser import TelemetryParser

class TelemetryListener(threading.Thread):
    def __init__(self, port, callback, status_callback=None, speed_callback=None, lap_callback=None, wear_callback=None, distance_callback=None):
        super().__init__()
        self.port = port
        self.callback = callback
        self.status_callback = status_callback
        self.speed_callback = speed_callback
        self.lap_callback = lap_callback
        self.wear_callback = wear_callback
        self.distance_callback = distance_callback
        self.running = False
        self.sock = None
        self.daemon = True
        self.last_track_id = -1
        self.last_speed = -1
        self.last_lap = -1
        self.total_laps = -1
        self.track_length = 0
        
    def stop(self):
        self.running = False
        if self.sock:
            try:
                dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dummy_sock.sendto(b'', ('127.0.0.1', self.port))
                dummy_sock.close()
            except: pass
            
    def run(self):
        self.running = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.settimeout(1.0)
            if self.status_callback: self.status_callback(f"Ouvindo porta {self.port}", "green")
            
            while self.running:
                try: data, addr = self.sock.recvfrom(2048)
                except socket.timeout: continue
                except Exception as e:
                    if self.running: print(f"Erro no socket: {e}")
                    break
                    
                self.process_packet(data)
        except Exception as e:
            if self.status_callback: self.status_callback(f"Erro porta {self.port}", "red")
        finally:
            if self.sock: self.sock.close()

    def process_packet(self, data):
        header = TelemetryParser.parse_header(data)
        if not header: return
        
        if header.m_packetId == 1:
            session = TelemetryParser.parse_session(data)
            if session:
                self.track_length = session.m_trackLength
                if session.m_trackId != self.last_track_id and session.m_trackId >= 0:
                    self.last_track_id = session.m_trackId
                    if self.callback: self.callback(session.m_trackId)
                if session.m_totalLaps != self.total_laps:
                    self.total_laps = session.m_totalLaps
                    
        elif header.m_packetId == 2:
            lap = TelemetryParser.parse_lap_data(data, header)
            if lap:
                if lap["curr_lap"] != self.last_lap and lap["curr_lap"] > 0:
                    print(f"LAP CHANGED: {self.last_lap} -> {lap['curr_lap']}")
                    self.last_lap = lap["curr_lap"]
                    if self.lap_callback: self.lap_callback(self.last_lap, self.total_laps)
                elif self.last_lap == -1:
                    print(f"FIRST LAP SEEN: {lap['curr_lap']}")
                    self.last_lap = lap["curr_lap"]
                    if self.lap_callback: self.lap_callback(self.last_lap, self.total_laps)
                if self.distance_callback and self.track_length > 0:
                    self.distance_callback(lap["lap_dist"], self.track_length)
                    
        if header.m_packetId == 6:
            tel = TelemetryParser.parse_car_telemetry(data, header)
            if tel:
                if "speed" in tel:
                    self.last_speed = tel["speed"]
                    if self.speed_callback: self.speed_callback(self.last_speed)
                if "wear" in tel and self.wear_callback:
                    self.wear_callback(tel["wear"])
                    
        is_damage = False
        if header.m_packetFormat >= 2025 and header.m_packetId == 10:
            is_damage = True
        elif 2021 <= header.m_packetFormat <= 2024 and header.m_packetId == 7:
            is_damage = True
            
        if is_damage:
            if header.m_packetFormat >= 2025 and not getattr(self, '_dumped_10', False):
                self._dumped_10 = True
                with open("udp_dump_10.bin", "wb") as f:
                    f.write(data)
                    
            dam = TelemetryParser.parse_car_damage(data, header)
            if dam and self.wear_callback:
                self.wear_callback(dam["wear"])
