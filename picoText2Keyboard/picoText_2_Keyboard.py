import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
#You may have to change this layout depending on your keyboard layout
from keyboard_layout_win_uk import KeyboardLayout
#from keyboard_layout_win_fr import KeyboardLayout #This is for a french keyboard for example.
from keycode_win_uk import Keycode
import digitalio
import board

filename = 'gspoc.txt'
delaySecs = 0.01

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
kbd = Keyboard(usb_hid.devices)
kbd_layout = KeyboardLayout(kbd)

#load a txt
def loadFile():    
    print('Loading file')
    data = open(filename,"r", encoding='utf')
    lines = open(filename, "r", encoding='utf8')
    lines = lines.readlines()
    print(len(lines))
    return data.read()

def typeOutString(inputstring, Stime):
    inputstring = str(inputstring)
    Stime = Stime
    count = 0
    key = ''
    for char in inputstring:
        led.value = True
        kbd_layout.write(char)
        time.sleep(Stime)  # Adjust the delay between key presses if necessary
        led.value = False

def ledSequence():    
    led.value = True
    print('You have 10 Seconds before code execution.')
    time.sleep(2)
    for i in range(0,30):
        if i < 10:
            time.sleep(0.2)
            led.value = False
            time.sleep(0.2)
            led.value = True
        if i == 8:
            print('5 Seconds before code execuition')
        if i > 10:   
            time.sleep(0.1)
            led.value = False
            time.sleep(0.1)
            led.value = True 
    print(f'''Running!\n''')

ledSequence()
typeOutString(loadFile(),delaySecs)
print('Done!')
led.value = False                                                                                                                                                                                                       