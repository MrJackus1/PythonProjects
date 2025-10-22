import network, socket, rp2, sys
from time import sleep


# Hash stuff
import uhashlib as hashlib
import os, struct

keyFile = 'key.txt'
counterFile = 'counter.txt'

# Sockets and Wifi
ssid = "Pico_AP"
passwd = "55554444"
server_ip = '192.168.4.1'
port = 8080
rp2.country('US')
# Change at your peril.
gateway_ip = '192.168.4.1'
accessPoint = ''
subnet = '255.255.255.0'


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
    return int(otp)

def readCounter(fileName='counter.txt'):
    with open(fileName) as f:
        counter = f.readline()
    print(f'''Counter is: {counter}''')
    return int(counter)

def saveCounter(counter='', fileName='counter.txt'):
    if counter == '':
        print('Trying to save a nul number...')
    else:           
        with open(fileName, 'w') as f:
            f.write(str(counter))
        print(f'''Counter saved: {counter}''')

def startWifi(name="Pico_AP", pw='12345678', ip="192.168.4.1", gateway='192.168.4.1', subnet="255.255.255.0", dns="8.8.8.8"):
    print("Starting Wifi network...")
    accessPoint = network.WLAN(network.AP_IF)
    accessPoint.active(False)
    sleep(1)
    accessPoint.config(essid=ssid, password=passwd)
    accessPoint.active(True)
    accessPoint.config(pm = 0xa11140)
    accessPoint.ifconfig((ip, subnet, gateway, dns))

    print(f'''Started - "{ssid}" - Server IP "{ip}"''')
    print(f'''{accessPoint.active(), accessPoint.ifconfig()}''')
    #print(accessPoint()[0])
    sleep(3)
          
def connection(port=80, key='key.txt', countFile='counter.txt'):
    address = socket.getaddrinfo("0.0.0.0", port,)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address))
    s.listen(10)
    while True:            
        #print(s)
        print(f'''Waiting for connection...''')
        client, address = s.accept()
        client.settimeout(5)
        #print(accessPoint.ifconfig())
        data = client.recv(1024)
        print(f'''Connection from: {address}\n''')
        data = data.decode('utf-8')
        data = data.split(':')
        print(f'''Data Receieved:\n{data}''')
        # Generate a code using the saved counter on this pico. If any of the next 10 match. Return 100 if not return 200
        count = readCounter(countFile)
        check = ''
        for i in range(11):
            #print(i)
            check = generateOTP(key, count+i)
            #print(type(int(data[0])))
            #print(type(check))
            if int(data[0]) == check:
                print('Sending 100')
                client.sendall('100')
                saveCounter((count + 1) + i)
        if int(data[0]) != check:
            client.sendall('200')
        else:
            client.sendall('404')
        client.close()

def readKey(key_file):
    try:
        with open(key_file) as f:
            key = f.readline()
            print(f'''Key loaded from "{key_file}"''')
        return key
    except:
        print("No file found containing key found. Closing AP. Create a key.txt in the root of the device. Put the key on line 1.")
        sys.close()

def main():
    try:
        key = readKey(keyFile)       
        startWifi(ssid, passwd, server_ip, gateway_ip)
        connection(port, key, counterFile)
    except KeyboardInterrupt as ki:
        print(f'''\nStopping server...''')

main()