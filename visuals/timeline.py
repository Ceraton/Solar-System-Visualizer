from datetime import date, timedelta

# J2000 epoch — January 1, 2000 at 12:00 TT
J2000_EPOCH = date(2000, 1, 1)


DAYS_PER_MINUTE = 365.25


class Timeline:
    def __init__(self):
        self.current_date = date.today()
        self.playing = False
        self.speed = DAYS_PER_MINUTE

    def tick(self, dt):
        if self.playing:
            days_elapsed = (dt / 1000) * (self.speed / 60)
            self.current_date += timedelta(days=days_elapsed)
    
    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def set_date(self, new_date):
        self.current_date = new_date

    def get_angle(self, planet):
        if planet.orbital_period_days == 0:
            return 0
        days_since_j2000 = (self.current_date - J2000_EPOCH).days
        degrees = planet.mean_longitude_deg + (360 / planet.orbital_period_days) * days_since_j2000
        return degrees % 360
