# Wifi & sockets
from time import sleep
from machine import Pin
import network, socket, rp2, sys, gc

# Hash
import uhashlib as hashlib
import os, struct

keyFile = 'key.txt'
counterFile = 'counter.txt'

# Wifi & sockets
rp2.country('US')
name = "Pico_AP"
password = "55554444"
ip = "192.168.4.25"
port = 8080

# Change at your peril.
gateway = "192.168.4.1"
subnet = "255.255.255.0"
dns = "0.0.0.0"

led = Pin('LED', Pin.OUT)
wlan = network.WLAN(network.STA_IF)

def generateHash(secretKey, counter, digits=6):
    counterBytes = struct.pack('>Q', counter)
    # Generate the hash HMAC-SHA1 with the counter.
    hash = hashlib.sha1(secretKey)
    # Update it with the counter in bytes.
    hash.update(counterBytes)
    # Create the hash.
    hmacResult = hash.digest()
    return hmacResult

def generateOTP(key, counter):
    # This will generate a One Time Passcode that we can send to the server or the server can use to generate one it self to confirm the code.
    hmac = generateHash(key, counter)
    offset = hmac[-1] & 0x0F
    lastFourBytes = hmac[offset: offset + 4]
    # Converts the 4 bytes into big endian 32 bit integer and the bitwise operation clears the sign bit so its always positive.
    number = struct.unpack('>I', lastFourBytes)[0] & 0x7FFFFFFF
    # Calculates the One Time Passcode and then converts it to a string with 0s padded at the front.
    otp = number % (10 ** 6)
    otp = str(otp)
    otp = f'''{otp:06}'''
    return otp

def readKey(fileName='key.txt'):
    try:
        with open(fileName) as f:
            key = f.readline()
        print(f'''Key loaded from "{fileName}"''')
        return key
    except:
        print("No file containing key found. Closing client. Create a key.txt in the root of the device. Put the key on line 1.")
        
def readCounter(fileName='counter.txt'):
    try:            
        with open(fileName) as f:
            counter = f.readline()
        print(f'''Counter is: {counter}''')
        return int(counter)
    except:
        print("No file containing counter found. Closing client. Create a counter.txt in the root of the device. Put the count on line 1.")
        sys.exit()

def saveCounter(counter='', fileName='counter.txt'):
    if counter == '':
        print('Trying to save a nul number...')
    else:           
        with open(fileName, 'w') as f:
            f.write(str(counter))
        print(f'''Counter saved: {counter}''')

def connectToNetwork(ssid, passwd, delay=0.5):
    #wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    sleep(1)
    wlan.active(True)
    print(f'''Config before: {wlan.ifconfig()}''')
    wlan.ifconfig((ip, subnet, gateway, dns))
    wlan.config(pm = 0xa11140)
    print(f'''Config after: {wlan.ifconfig()}''')
    wlan.connect(ssid, passwd)
    print(f'''Connecting to '{ssid}'...''')
    while not wlan.isconnected():
        sleep(delay)
        led.toggle()
        #wlan.connect(ssid, passwd)
    print(f'''Connected to: {wlan.ifconfig()}''')

def sendMessage(hotp='0000', message='Hello World!', counter='', ip="192.168.4.1", port=8080):
    if wlan.isconnected():
        message = f'''{hotp}:{message}'''
        print(f'''Sending message: "{message}"''')
        msg = bytes(message, 'utf-8')
        s = socket.socket()
        s.settimeout(30)
        s.connect(socket.getaddrinfo(ip, port)[0][-1])
        s.sendall(msg)
        reply, addr = s.recvfrom(1024)
        reply = reply.decode('utf-8')
        print(f'''Server Reply: {reply}''')
        if reply == '100':
            saveCounter(counter + 1)
            print('Authorised.')
            return 100
        elif reply == '200':
            print('Not authorised.')
            return 200
        else:
            print('Error. Not authorised.')
            return 404
        s.close()
    else:
        print('Wifi not connected :(')

def main():        
    connectToNetwork(name, password, 0.5)
    sleep(1)
    key = readKey(keyFile)
    while True:
        counter = readCounter(counterFile)
        msg = input("Message: ")
        sendMessage(generateOTP(key, counter), msg, counter)
        gc.collect()
        
main()
