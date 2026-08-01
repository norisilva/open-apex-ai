class TyrePredictor:
    def __init__(self):
        self.wear_history = {} # lap_num -> (rl, rr, fl, fr)
        self.current_wear = (0.0, 0.0, 0.0, 0.0)
        self.wear_per_lap = (0.0, 0.0, 0.0, 0.0)
        self.current_lap = -1
        self.total_laps = -1
        self.pit_threshold = 65.0
        
    def update_wear(self, wear_data):
        self.current_wear = wear_data
        
    def update_lap(self, lap_num, total_laps):
        self.total_laps = total_laps
        
        # Calculate delta from previous lap
        if self.current_lap != -1 and self.current_lap != lap_num:
            if self.current_lap in self.wear_history:
                prev = self.wear_history[self.current_lap]
                curr = self.current_wear
                
                # Calculate delta for each tyre
                delta = tuple(max(0, curr[i] - prev[i]) for i in range(4))
                
                # Avoid calculating on outlaps or reset laps (like when changing tyres, wear drops)
                if sum(delta) > 0 and max(delta) < 15.0:
                    # Basic smoothing (exponential moving average)
                    if sum(self.wear_per_lap) == 0.0:
                        self.wear_per_lap = delta
                    else:
                        alpha = 0.3 # 30% weight to new lap
                        self.wear_per_lap = tuple(
                            self.wear_per_lap[i] * (1 - alpha) + delta[i] * alpha 
                            for i in range(4)
                        )
        
        self.current_lap = lap_num
        self.wear_history[lap_num] = self.current_wear
        
    def get_predictions(self):
        """Returns predictions based on the worst performing tyre."""
        if sum(self.wear_per_lap) <= 0.01:
            if self.current_lap != -1:
                return {"is_calibrating": True}
            return None # Not enough data
            
        worst_current = max(self.current_wear)
        worst_index = self.current_wear.index(worst_current)
        worst_rate = self.wear_per_lap[worst_index]
        
        if worst_rate <= 0:
            if self.current_lap != -1:
                return {"is_calibrating": True}
            return None
            
        next_lap = worst_current + worst_rate
        in_5 = worst_current + (worst_rate * 5)
        
        laps_remaining = max(0, self.total_laps - self.current_lap)
        end_race = worst_current + (worst_rate * laps_remaining)
        
        # Pit stop suggestion
        wear_left = max(0, self.pit_threshold - worst_current)
        laps_to_pit = int(wear_left / worst_rate)
        suggested_pit_lap = self.current_lap + laps_to_pit
        
        # If suggested pit lap is beyond total laps, no stop needed
        pit_str = str(suggested_pit_lap)
        if self.total_laps > 0 and suggested_pit_lap > self.total_laps:
            pit_str = "S/ Parada"
        elif wear_left <= 0:
            pit_str = "BOX AGORA!"
            
        return {
            "is_calibrating": False,
            "current": self.current_wear,
            "next_lap": next_lap,
            "in_5_laps": in_5,
            "end_race": end_race,
            "suggested_pit": pit_str,
            "worst_rate": worst_rate,
            "worst_current": worst_current
        }
