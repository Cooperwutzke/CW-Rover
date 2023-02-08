from machine import Pin, I2C, SPI
from nrf24l01 import NRF24L01
import utime
import struct

led = machine.Pin(25, mode=Pin.OUT)

# Sender SPI
spi_sck = machine.Pin(18)
spi_tx = machine.Pin(19)
spi_rx = machine.Pin(16)
spi_csn = machine.Pin(17, mode=Pin.OUT, value=1)
spi_ce = machine.Pin(20, mode=Pin.OUT, value=0)

# Receiver SPI
# spi_sck = machine.Pin(2)
# spi_tx = machine.Pin(3)
# spi_rx = machine.Pin(0)
# spi_csn = machine.Pin(1, mode=Pin.OUT, value=1)
# spi_ce = machine.Pin(8, mode=Pin.OUT, value=0)


spi = SPI(0, sck=spi_sck, mosi=spi_tx, miso=spi_rx, baudrate=1000000)
payload_size = 12

# Define the channel or 'pipes' the radios use.
# switch around the pipes depending if this is a sender or receiver pico

role = "send"
#role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    
def setup_nrf():
    print("Initializing the nRF24L01 Module...")
    nrf = NRF24L01(spi, spi_csn, spi_ce, payload_size=payload_size)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf

def send(nrf, msg):
    print("Sending message [", msg, "]")
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            print(role, "Message [", msg[n], "sent")
            flash_led(1)
        except OSError:
            print(role, "Error sending message")
    nrf.send("\n")
    nrf.start_listening()
    
def flash_led(times:int=None):
    for _ in range(times):
        led.value(1)
        utime.sleep_ms(1)
        led.value(0)
        utime.sleep_ms(1)


nrf = setup_nrf()
msg_string = ""
nrf.start_listening()

while 1:
    if role == "send":
        send(nrf, "Hello World!")
        send(nrf, "Test")
    else:
        # Check for messages
        if nrf.any():
            package = nrf.recv()
            message = struct.unpack("s", package)
            msg = message[0].decode()
            flash_led(1)
        
        # Check for newline character; End of message or out of space
        try:
            if (msg == "\n") and (len(msg_string) <= 20):
                print("Full message: ", msg_string, msg)
                msg_string = ""
            else:
                if len(msg_string) <= 20:
                    msg_string = msg_string + msg
                else:
                    msg_string = ""
        except NameError:
            print("No Message found...")