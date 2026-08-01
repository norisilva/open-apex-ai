import ctypes

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

class CarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_speed', ctypes.c_uint16),
        ('m_padding', ctypes.c_uint8 * 58)
    ]

class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carTelemetryData', CarTelemetryData * 22),
    ]
