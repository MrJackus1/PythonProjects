# Pico 2 Pico Rolling code or Hashed One Time Passcode authentication.
 Authenticates messages from another Pi Pico using HOTP SHA1 authentication.
 A basic implementation of peer to peer SHA1 message authentication.<br>
</br>
Uses a shared key. So make sure the key.txt has the same key and the counter.txt has the same counter. Client can be up-to 10 counts forward to account for de-sync. Not so import with TCP but definetly with radio transmissions.</br>
</br>
Make sure to copy all files to the root of your pico. Start the Access Point (Pico_AP.py) first. Then once its waiting for a connection. Start your client (Pico_Client.py).</br>
<br>
You will need two Pi Pico Ws or Pi Pico W 2's. Or a mix.
