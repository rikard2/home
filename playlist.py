import datetime

autumn_chill                    = 'spotify:user:mariokristian:playlist:7G8qKmsQOGyguhiEo2o8bl'
sleep_tight                     = 'spotify:user:spotify:playlist:37i9dQZF1DWZd79rJ6a7lp'
house                           = 'spotify:user:mejoresplaylistsspotify:playlist:2DZvLW8oBFRLa2c1uju3oy'

def choose(hour = datetime.datetime.now().hour, weekday = datetime.datetime.now().isoweekday()):
    print(hour, weekday)
    if 5 <= weekday <= 6 and 19 <= hour < 22:
        print("Party!")
        return house
    elif 17 <= hour < 22:
        print("I choose autumn_chill")
        return autumn_chill
    elif 22 < hour < 24:
        print("Let's go to sleep...")
        return sleep_tight

    print("I dont want music... :(")
    return None
