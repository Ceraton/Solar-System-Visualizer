from datetime import date, timedelta

# J2000 epoch — January 1, 2000 at 12:00 TT
J2000_EPOCH = date(2000, 1, 1)


DAYS_PER_MINUTE = 365.25


class Timeline:
    def __init__(self):
        self.start_date = J2000_EPOCH
        self.current_date = 0.0
        self.playing = True
        self.speed = 1

    def tick(self, dt):
        if self.playing:
            self.current_date += (dt / 1000.0) * self.speed
    
    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def set_date(self, new_date):
        self.current_date = new_date

    def get_angle(self, planet):
        if planet.orbital_period_days == 0:
            return 0
        motion = (360.0 / planet.orbital_period_days) * self.current_date
        return (planet.mean_longitude_deg + motion) % 360
    
    def get_atomic_date(self):
        target_date = self.start_date + timedelta(days=self.current_date)
        return target_date.strftime("%b %d, %Y | %H:%M")
