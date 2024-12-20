class Setting:
    def __init__(self):
        self.screen_width=1200
        self.screen_height=700
        self.bg_color=(255,255,255)
        self.ship_limit=3
        
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullet_allowed=3
    
        self.fleet_drop_speed=3
        self.score_scale=1.5
        self.alein_points=50
    
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.fleet_direction=1
        self.speedup_scale=1.1
        self.alein_speed_factor=1
        self.ship_speed_factor=1.5
        
    
    def increase_speed(self):
        self.ship_speed_factor *=self.speedup_scale
        self.alein_speed_factor *=self.speedup_scale
        self.bullet_speed_factor *=self.speedup_scale
        self.alein_points=int(self.alein_points*self.score_scale)
        
        
        
        
        