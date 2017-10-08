import pytz
from datetime import datetime, timedelta

autumn_sounds                   = 'spotify:user:spotify:playlist:37i9dQZF1DX4H7FFUM2osB'
autumn_chill                    = 'spotify:user:mariokristian:playlist:7G8qKmsQOGyguhiEo2o8bl'
sleep_tight                     = 'spotify:user:spotify:playlist:37i9dQZF1DWZd79rJ6a7lp'
house                           = 'spotify:user:mejoresplaylistsspotify:playlist:2DZvLW8oBFRLa2c1uju3oy'

stockholmtz = pytz.timezone('Europe/Stockholm')

def choose(hour = -1, weekday = -1):
    if hour == -1:
        hour = ( datetime.utcnow() + timedelta(hours=2) ).hour
    if weekday == -1:
        weekday = ( datetime.utcnow() + timedelta(hours=2) ).isoweekday()
    if 5 <= weekday <= 6 and 19 <= hour < 22:
        print("Party!")
        return house
    elif weekday == 7 and 15 <= hour < 17:
        print("Sunday chill")
        return autumn_sounds
    elif 17 <= hour < 22:
        print("I choose autumn_chill")
        return autumn_chill
    elif 22 < hour < 24:
        print("Let's go to sleep...")
        return sleep_tight

    print("I dont want music... :(")
    return None
