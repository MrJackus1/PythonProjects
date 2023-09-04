import time, os
from winotify import Notification

titleIs = "Eye Strain Reminder"
message = "Its been 20 Minutes since your last eye break. Please look out the window for 20 seconds!"
durationSeconds = 'short' 
iconPath = "icon.png"
intervalsMins = 20


path = str(os.path.abspath(iconPath))
intervalsMins = intervalsMins * 60
#print(path)

alert = Notification(app_id="Eye Helper Outerer", title=titleIs, msg=message, icon=path, duration=durationSeconds)

while True:
    
    alert.show()
    time.sleep(intervalsMins)