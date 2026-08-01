import struct
import ctypes
from core.telemetry.packets import *

class TelemetryParser:
    @staticmethod
    def parse_header(data):
        if len(data) < 29: return None
        return PacketHeader.from_buffer_copy(data[:29])
        
    @staticmethod
    def parse_session(data):
        if len(data) < ctypes.sizeof(PacketSessionData): return None
        return PacketSessionData.from_buffer_copy(data)
        
    @staticmethod
    def parse_lap_data(data, header):
        h_size = 24 if header.m_packetFormat == 2020 else 29
        if len(data) <= h_size: return None
        idx = header.m_playerCarIndex
        if idx >= 22: return None
        
        struct_size = (len(data) - h_size) // 22
        offset = h_size + idx * struct_size
        
        fmt = header.m_packetFormat
        if fmt == 2020:
            lap_offset, dist_offset = 45, 32
        elif fmt == 2021:
            lap_offset, dist_offset = 25, 12
        elif fmt == 2022:
            lap_offset, dist_offset = 33, 20
        elif fmt == 2023:
            lap_offset, dist_offset = 31, 18
        elif fmt >= 2024:
            lap_offset, dist_offset = 33, 20
        else:
            lap_offset, dist_offset = 31, 18
            
        if len(data) >= offset + lap_offset + 1:
            curr_lap = struct.unpack_from('<B', data, offset + lap_offset)[0]
            lap_dist = struct.unpack_from('<f', data, offset + dist_offset)[0]
            return {"curr_lap": curr_lap, "lap_dist": lap_dist}
        return None

    @staticmethod
    def parse_car_telemetry(data, header):
        h_size = 24 if header.m_packetFormat == 2020 else 29
        if len(data) <= h_size: return None
        idx = header.m_playerCarIndex
        if idx >= 22: return None
        
        struct_size = (len(data) - h_size) // 22
        offset = h_size + idx * struct_size
        
        res = {}
        if len(data) >= offset + 2:
            res["speed"] = struct.unpack_from('<H', data, offset)[0]
            
        if header.m_packetFormat == 2020 and len(data) >= offset + 57:
            rl, rr, fl, fr = struct.unpack_from('<BBBB', data, offset + 53)
            res["wear"] = (float(rl), float(rr), float(fl), float(fr))
            
        return res if res else None

    @staticmethod
    def parse_car_damage(data, header):
        if header.m_packetFormat == 2020: return None
        
        h_size = 29
        if len(data) <= h_size: return None
        idx = header.m_playerCarIndex
        if idx >= 22: return None
        
        struct_size = (len(data) - h_size) // 22
        offset = h_size + idx * struct_size
        
        if len(data) >= offset + 16:
            rl, rr, fl, fr = struct.unpack_from('<ffff', data, offset)
            return {"wear": (rl, rr, fl, fr)}
        return None
