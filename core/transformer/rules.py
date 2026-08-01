RULES = {
    # Suspensão: reduzir 25% (meio do range 20-30%) 
    # Objetivo: absorver zebras, suavizar volante e evitar snap na zebras.
    "suspension": {
        "front_suspension":     {"factor": 0.75, "min": 1, "max": 41, "round": True},
        "rear_suspension":      {"factor": 0.75, "min": 1, "max": 41, "round": True},
        "front_anti_roll_bar":  {"factor": 0.75, "min": 1, "max": 21, "round": True},
        "rear_anti_roll_bar":   {"factor": 0.75, "min": 1, "max": 21, "round": True},
        # Ride height: NÃO reduzir (afeta aero)
    },
    
    # Transmissão: travar differencial para evitar snap oversteer
    "transmission": {
        # Travar limite a 52% max para on-throttle (pode ser ajustado)
        "on_throttle":  {"clamp_max": 52, "clamp_min": 50},
        # Off throttle garante rotação na entrada da curva sem esforço exagerado
        "off_throttle": {"clamp_max": 65, "clamp_min": 50},
    },
    
    # Pneus: reduzir 0.5 PSI para mais grip mecânico (estabilidade)
    "tyres": {
        "front_right_pressure": {"offset": -0.5, "min": 21.0, "max": 29.5},
        "front_left_pressure":  {"offset": -0.5, "min": 21.0, "max": 29.5},
        "rear_right_pressure":  {"offset": -0.5, "min": 21.0, "max": 26.5},
        "rear_left_pressure":   {"offset": -0.5, "min": 21.0, "max": 26.5},
    },
    
    # Aerodinâmica: PRESERVAR (não alterar)
    "aerodynamics": None,
    
    # Geometria da suspensão: PRESERVAR
    "suspension_geometry": None,
    
    # Freios: reduzir pressão levemente (menos esforço de frenagem no braço)
    "brakes": {
        "brake_pressure":    {"offset": -5, "min": 80, "max": 100},
    },
}
