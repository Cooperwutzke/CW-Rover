#  *  Cooper Wutzke
#  *  Mobility Code for CW-Remote
#  *  10/4/2022
#  *  
#  *  Raspberry Pi Pico
#  *  
#  *  All Peripherals:
#  *  - Wii Nunchuck for input
#  *  - NRF24L01 2.4Ghz Transceiver
#  *  - 1 ADC for battery voltage monitor
#  *  - SSD1306 0.96" OLED

from machine import Pin, I2C
from nrf24l01 import NRF24L01
import struct
import ssd1306
import utime
import framebuf
import nunchuck

I2C_SDA_PIN = machine.Pin(4, machine.Pin.PULL_UP)
I2C_SCL_PIN = machine.Pin(5, machine.Pin.PULL_UP)

led = machine.Pin(25, mode=Pin.OUT)
i2c = machine.I2C(0,sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=300000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
nun = nunchuck.Nunchuck(machine.I2C(1,
        scl=machine.Pin(7, machine.Pin.PULL_UP),
        sda=machine.Pin(6, machine.Pin.PULL_UP),
        freq=100000
        ))

spi_csn = machine.Pin(17, mode=Pin.OUT, value=1)
spi_ce = machine.Pin(20, mode=Pin.OUT, value=0)
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
    nrf = NRF24L01(SPI(0), spi_csn, spi_ce, payload_size=payload_size)
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

def display_draw():
    display_draw_diag()
    display_draw_chuck()
    
def display_draw_diag():
    draw_battery(x, y)
    
def draw_battery(x, y):
    # Batt Top
    display.hline(x, y, 12, 1)
    display.hline(x, y+1, 12, 1)
    # Batt Middle
    display.vline(x, y+2, 4, 1)
    display.vline(x+1, y+2, 4, 1)
    display.vline(x+12, y+2, 4, 1)
    display.vline(x+13, y+2, 4, 1)
    display.pixel(x+10, y+2, 1)
    display.pixel(x+11, y+2, 1)
    display.pixel(x+10, y+5, 1)
    display.pixel(x+11, y+5, 1)
    # Batt Bottom
    display.hline(x, y+6, 12, 1)
    display.hline(x, y+7, 12, 1)
    display.show()

def draw_cbutton(x, y, toggled_on):
    #C Button Border
    ##Top Bar
    display.hline(x+5, y, 8, 1)
    display.hline(x+5, y+1, 8, 1)
    
    ##First Squares at Y+1
    display.vline(x+3, y+1, 4, 1)
    display.vline(x+4, y+1, 2, 1)
    display.vline(x+13, y+1, 2, 1)
    display.vline(x+14, y+1, 4, 1)
    
    ##Second Squares at Y+3
    display.vline(x+2, y+3, 4, 1)
    display.vline(x+15, y+3, 4, 1)
    
    ##Third Squares at Y+5
    display.vline(x+1, y+5, 8, 1)
    display.vline(x+16, y+5, 8, 1)
    
    #Sides
    display.vline(x, y+7, 4, 1)
    display.vline(x+17, y+7, 4, 1)
    
    ##Fourth Squares at Y+11
    display.vline(x+2, y+11, 4, 1)
    display.vline(x+15, y+11, 4, 1)
    
    ##Fifth Squares at Y+13
    display.vline(x+3, y+13, 4, 1)
    display.vline(x+14, y+13, 4, 1)
    
    #Sixth Squares at Y+15
    display.vline(x+4, y+15, 2, 1)
    display.vline(x+13, y+15, 2, 1)
    
    ##Bottom Bar
    display.hline(x+5, y+17, 8, 1)
    display.hline(x+5, y+16, 8, 1)
    
    if (toggled_on == 0):
        # C Button Fill
        display.fill_rect(x+4, y+3, 10, 12, 0)
        display.hline(x+5, y+2, 8, 0)
        display.hline(x+5, y+15, 8, 0)
        display.vline(x+3, y+5, 8, 0)
        display.vline(x+14, y+5, 8, 0)
        display.vline(x+15, y+7, 4, 0)
        display.vline(x+2, y+7, 4, 0)
        
        # C Button Letter
        display.hline(x+7, y+4, 4, 1)
        display.hline(x+6, y+5, 6, 1)
        display.vline(x+6, y+5, 8, 1)
        display.vline(x+7, y+5, 8, 1)
        #display.vline(x+5, y+8, 2, 1)
        display.hline(x+6, y+12, 4, 1)
        display.hline(x+6, y+12, 6, 1) 
        display.hline(x+7, y+13, 4, 1)
    else:
        # C Button Fill
        display.fill_rect(x+2, y+3, 14, 12, 1)
        display.hline(x+5, y+2, 8, 1)
        display.hline(x+5, y+15, 8, 1)
        
        #C Button Letter Inverted
        display.hline(x+7, y+4, 4, 0)
        display.hline(x+6, y+5, 6, 0)
        display.vline(x+6, y+5, 8, 0)
        display.vline(x+7, y+5, 8, 0)
        #display.vline(x+5, y+8, 2, 0)
        display.hline(x+6, y+12, 4, 0)
        display.hline(x+6, y+12, 6, 0) 
        display.hline(x+7, y+13, 4, 0)
    display.show()

def draw_zbutton(x, y, toggled_on):
    # Z Button Border
    ## Top Bar
    display.hline(x+2, y, 14, 1)
    display.hline(x+1, y+1, 16, 1)
    ## Curve Fills
    display.vline(x+2, y+2, 2, 1)
    display.vline(x+15, y+2, 2, 1)
    display.vline(x+2, y+14, 2, 1)
    display.vline(x+15, y+14, 2, 1)
    ## Left Side
    display.vline(x+1, y+1, 16, 1)
    display.vline(x, y+3, 12, 1)
    ## Right Side
    display.vline(x+16, y+1, 16, 1)
    display.vline(x+17, y+3, 12, 1)
    ## Bottom Bar
    display.hline(x+1, y+16, 16, 1)
    display.hline(x+2, y+17, 14, 1)
    
    if (toggled_on == 0):
        # Z Button Fill
        display.fill_rect(x+2, y+2, 14, 14, 0)
        
        # Z Button Letter
        display.hline(x+5, y+4, 8, 1)
        display.hline(x+5, y+5, 8, 1)
        display.hline(x+10, y+6, 3, 1)
        display.hline(x+9, y+7, 3, 1)
        display.hline(x+8, y+8, 3, 1)
        display.hline(x+8, y+9, 2, 1)
        display.hline(x+7, y+10, 3, 1)
        display.hline(x+6, y+11, 3, 1)
        display.hline(x+5, y+12, 8, 1)
        display.hline(x+5, y+13, 8, 1)
    else:
        # Z Button Fill
        display.fill_rect(x+2, y+2, 14, 14, 1)
        
        # Z Button Letter Inverted
        display.hline(x+5, y+4, 8, 0)
        display.hline(x+5, y+5, 8, 0)
        display.hline(x+10, y+6, 3, 0)
        display.hline(x+9, y+7, 3, 0)
        display.hline(x+8, y+8, 3, 0)
        display.hline(x+8, y+9, 2, 0)
        display.hline(x+7, y+10, 3, 0)
        display.hline(x+6, y+11, 3, 0)
        display.hline(x+5, y+12, 8, 0)
        display.hline(x+5, y+13, 8, 0)
    display.show()
    
def draw_uparrow(x, y, toggled_on):
    # Arrow Outline
    display.hline(x, y+15, 30, 1)
    display.hline(x, y+14, 30, 1)
    display.hline(x+1, y+13, 3, 1)
    display.hline(x+1, y+12, 3, 1)
    display.hline(x+3, y+11, 3, 1)
    display.hline(x+3, y+10, 3, 1)
    display.hline(x+5, y+9, 3, 1)
    display.hline(x+5, y+8, 3, 1)
    display.hline(x+7, y+7, 3, 1)
    display.hline(x+7, y+6, 3, 1)
    display.hline(x+9, y+5, 3, 1)
    display.hline(x+9, y+4, 3, 1)
    display.hline(x+11, y+3, 3, 1)
    display.hline(x+11, y+2, 8, 1)
    display.hline(x+13, y+1, 4, 1)
    display.hline(x+16, y+3, 3, 1)
    display.hline(x+18, y+4, 3, 1)
    display.hline(x+18, y+5, 3, 1)
    display.hline(x+20, y+6, 3, 1)
    display.hline(x+20, y+7, 3, 1)
    display.hline(x+22, y+8, 3, 1)
    display.hline(x+22, y+9, 3, 1)
    display.hline(x+24, y+10, 3, 1)
    display.hline(x+24, y+11, 3, 1)
    display.hline(x+26, y+12, 3, 1)
    display.hline(x+26, y+13, 3, 1)
    if (toggled_on == 0):
        display.hline(x+4, y+13, 22, 0)
        display.hline(x+4, y+12, 22, 0)
        display.hline(x+6, y+11, 18, 0)
        display.hline(x+6, y+10, 18, 0)
        display.hline(x+8, y+9, 14, 0)
        display.hline(x+8, y+8, 14, 0)
        display.hline(x+10, y+7, 10, 0)
        display.hline(x+10, y+6, 10, 0)
        display.hline(x+12, y+5, 6, 0)
        display.hline(x+12, y+4, 6, 0)
        display.hline(x+14, y+3, 2, 0)
    else:
        display.hline(x+1, y+13, 28, 1)
        display.hline(x+1, y+12, 28, 1)
        display.hline(x+3, y+11, 24, 1)
        display.hline(x+3, y+10, 24, 1)
        display.hline(x+5, y+9, 20, 1)
        display.hline(x+5, y+8, 20, 1)
        display.hline(x+7, y+7, 16, 1)
        display.hline(x+7, y+6, 16, 1)
        display.hline(x+9, y+5, 12, 1)
        display.hline(x+9, y+4, 12, 1)
        display.hline(x+11, y+3, 8, 1)
    display.show()
    
def draw_downarrow(x, y, toggled_on):
    display.hline(x, y, 30, 1)
    display.hline(x, y+1, 30, 1)
    display.hline(x+1, y+2, 3, 1)
    display.hline(x+1, y+3, 3, 1)
    display.hline(x+3, y+4, 3, 1)
    display.hline(x+3, y+5, 3, 1)
    display.hline(x+5, y+6, 3, 1)
    display.hline(x+5, y+7, 3, 1)
    display.hline(x+7, y+8, 3, 1)
    display.hline(x+7, y+9, 3, 1)
    display.hline(x+9, y+10, 3, 1)
    display.hline(x+9, y+11, 3, 1)
    display.hline(x+11, y+12, 3, 1)
    display.hline(x+11, y+13, 8, 1)
    display.hline(x+13, y+14, 4, 1)
    display.hline(x+16, y+12, 3, 1)
    display.hline(x+18, y+11, 3, 1)
    display.hline(x+18, y+10, 3, 1)
    display.hline(x+20, y+9, 3, 1)
    display.hline(x+20, y+8, 3, 1)
    display.hline(x+22, y+7, 3, 1)
    display.hline(x+22, y+6, 3, 1)
    display.hline(x+24, y+5, 3, 1)
    display.hline(x+24, y+4, 3, 1)
    display.hline(x+26, y+3, 3, 1)
    display.hline(x+26, y+2, 3, 1)
    if (toggled_on == 0):
        display.hline(x+4, y+2, 22, 0)
        display.hline(x+4, y+3, 22, 0)
        display.hline(x+6, y+4, 18, 0)
        display.hline(x+6, y+5, 18, 0)
        display.hline(x+8, y+6, 14, 0)
        display.hline(x+8, y+7, 14, 0)
        display.hline(x+10, y+8, 10, 0)
        display.hline(x+10, y+9, 10, 0)
        display.hline(x+12, y+10, 6, 0)
        display.hline(x+12, y+11, 6, 0)
        display.hline(x+14, y+12, 2, 0)
    else:
        display.hline(x+1, y+2, 28, 1)
        display.hline(x+1, y+3, 28, 1)
        display.hline(x+3, y+4, 24, 1)
        display.hline(x+3, y+5, 24, 1)
        display.hline(x+5, y+6, 20, 1)
        display.hline(x+5, y+7, 20, 1)
        display.hline(x+7, y+8, 16, 1)
        display.hline(x+7, y+9, 16, 1)
        display.hline(x+9, y+10, 12, 1)
        display.hline(x+9, y+11, 12, 1)
        display.hline(x+11, y+12, 8, 1)
    display.show()
    
def draw_leftarrow(x, y, toggled_on):
        # Right Side
        display.hline(x+16, y+10, 25, 1)
        display.hline(x+16, y+11, 25, 1)
        display.vline(x+40, y+10, 13, 1)
        display.vline(x+41, y+10, 13, 1)
        display.hline(x+16, y+22, 25, 1)
        display.hline(x+16, y+23, 25, 1)
        display.vline(x+16, y, 12, 1)
        display.vline(x+17, y, 12, 1)
        display.vline(x+16, y+22, 12, 1)
        display.vline(x+17, y+22, 12, 1)
        
        # Top Arrow Outline
        display.vline(x+15, y+2, 2, 1)
        display.vline(x+14, y+2, 4, 1)
        display.vline(x+13, y+4, 2, 1)
        display.vline(x+12, y+4, 4, 1)
        display.vline(x+11, y+6, 2, 1)
        display.vline(x+10, y+6, 4, 1)
        display.vline(x+9, y+8, 2, 1)
        display.vline(x+8, y+8, 4, 1)
        display.vline(x+7, y+10, 2, 1)
        display.vline(x+6, y+10, 4, 1)
        display.vline(x+5, y+12, 2, 1)
        display.vline(x+4, y+12, 4, 1)
        display.vline(x+3, y+14, 6, 1)
        display.vline(x+2, y+14, 6, 1)
        
        # Bottom Arrow Outline
        display.vline(x+15, y+30, 2, 1)
        display.vline(x+14, y+28, 4, 1)
        display.vline(x+13, y+28, 2, 1)
        display.vline(x+12, y+26, 4, 1)
        display.vline(x+11, y+26, 2, 1)
        display.vline(x+10, y+24, 4, 1)
        display.vline(x+9, y+24, 2, 1)
        display.vline(x+8, y+22, 4, 1)
        display.vline(x+7, y+22, 2, 1)
        display.vline(x+6, y+20, 4, 1)
        display.vline(x+5, y+20, 2, 1)
        display.vline(x+4, y+18, 4, 1)
        
        if (toggled_on == 0):
            display.fill_rect(x+16, y+12, 24, 10, 0)
            display.vline(x+15, y+4, 26, 0)
            display.vline(x+14, y+6, 22, 0)
            display.vline(x+13, y+6, 22, 0)
            display.vline(x+12, y+8, 18, 0)
            display.vline(x+11, y+8, 18, 0)
            display.vline(x+10, y+10, 14, 0)
            display.vline(x+9, y+10, 14, 0)
            display.vline(x+8, y+12, 10, 0)
            display.vline(x+7, y+12, 10, 0)
            display.vline(x+6, y+14, 6, 0)
            display.vline(x+5, y+14, 6, 0)
            display.vline(x+4, y+16, 2, 0)
        else:
            display.fill_rect(x+16, y+12, 24, 10, 1)
            display.vline(x+15, y+4, 26, 1)
            display.vline(x+14, y+6, 22, 1)
            display.vline(x+13, y+6, 22, 1)
            display.vline(x+12, y+8, 18, 1)
            display.vline(x+11, y+8, 18, 1)
            display.vline(x+10, y+10, 14, 1)
            display.vline(x+9, y+10, 14, 1)
            display.vline(x+8, y+12, 10, 1)
            display.vline(x+7, y+12, 10, 1)
            display.vline(x+6, y+14, 6, 1)
            display.vline(x+5, y+14, 6, 1)
            display.vline(x+4, y+16, 2, 1)
        display.show()
def draw_rightarrow(x, y, toggled_on):
        # Left Side
        display.hline(x, y+10, 25, 1)
        display.hline(x, y+11, 25, 1)
        display.vline(x, y+10, 13, 1)
        display.vline(x+1, y+10, 13, 1)
        display.hline(x, y+22, 25, 1)
        display.hline(x, y+23, 25, 1)
        display.vline(x+24, y, 12, 1)
        display.vline(x+25, y, 12, 1)
        display.vline(x+24, y+22, 12, 1)
        display.vline(x+25, y+22, 12, 1)
        
        # Top Arrow Outline
        display.vline(x+26, y+2, 2, 1)
        display.vline(x+27, y+2, 4, 1)
        display.vline(x+28, y+4, 2, 1)
        display.vline(x+29, y+4, 4, 1)
        display.vline(x+30, y+6, 2, 1)
        display.vline(x+31, y+6, 4, 1)
        display.vline(x+32, y+8, 2, 1)
        display.vline(x+33, y+8, 4, 1)
        display.vline(x+34, y+10, 2, 1)
        display.vline(x+35, y+10, 4, 1)
        display.vline(x+36, y+12, 2, 1)
        display.vline(x+37, y+12, 4, 1)
        display.vline(x+38, y+14, 6, 1)
        display.vline(x+39, y+14, 6, 1)
        
        # Bottom Arrow Outline
        display.vline(x+26, y+30, 2, 1)
        display.vline(x+27, y+28, 4, 1)
        display.vline(x+28, y+28, 2, 1)
        display.vline(x+29, y+26, 4, 1)
        display.vline(x+30, y+26, 2, 1)
        display.vline(x+31, y+24, 4, 1)
        display.vline(x+32, y+24, 2, 1)
        display.vline(x+33, y+22, 4, 1)
        display.vline(x+34, y+22, 2, 1)
        display.vline(x+35, y+20, 4, 1)
        display.vline(x+36, y+20, 2, 1)
        display.vline(x+37, y+18, 4, 1)
        
        if (toggled_on == 0):
            display.fill_rect(x+2, y+12, 24, 10, 0)
            display.vline(x+26, y+4, 26, 0)
            display.vline(x+27, y+6, 22, 0)
            display.vline(x+28, y+6, 22, 0)
            display.vline(x+29, y+8, 18, 0)
            display.vline(x+30, y+8, 18, 0)
            display.vline(x+31, y+10, 14, 0)
            display.vline(x+32, y+10, 14, 0)
            display.vline(x+33, y+12, 10, 0)
            display.vline(x+34, y+12, 10, 0)
            display.vline(x+35, y+14, 6, 0)
            display.vline(x+36, y+14, 6, 0)
            display.vline(x+37, y+16, 2, 0)
        else:
            display.fill_rect(x+2, y+12, 24, 10, 1)
            display.vline(x+26, y+4, 26, 1)
            display.vline(x+27, y+6, 22, 1)
            display.vline(x+28, y+6, 22, 1)
            display.vline(x+29, y+8, 18, 1)
            display.vline(x+30, y+8, 18, 1)
            display.vline(x+31, y+10, 14, 1)
            display.vline(x+32, y+10, 14, 1)
            display.vline(x+33, y+12, 10, 1)
            display.vline(x+34, y+12, 10, 1)
            display.vline(x+35, y+14, 6, 1)
            display.vline(x+36, y+14, 6, 1)
            display.vline(x+37, y+16, 2, 1)
        display.show()
        
def i2c_scan():
    print('Scanning I2C bus.')
    devices = i2c.scan() # this returns a list of devices

    device_count = len(devices)

    if device_count == 0:
        print('No i2c device found.')
    else:
        print(device_count, 'devices found.')

    for device in devices:
        print('Decimal address:', device, ", Hex address: ", hex(device))
        
#def draw_wireless(x, y):

nrf = setup_nrf()
msg_string = ""
while 1:
    # OLED using default address 0x3C
    # Nunchuck using default address 0x52
    
    nrf.start_listening()
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
        if (msg == "\n") and (len(msg_string) <= 20):
            print("Full message: ", msg_string, msg)
            msg_string = ""
        else:
            if len(msg_string) <= 20:
                msg_string = msg_string + msg
            else:
                msg_string = ""
    
    draw_battery(110, 0)
    
    buttons = nun.buttons()
    print(buttons[0])
    print(buttons[1])
    if buttons[0] == True:
        draw_cbutton(30, 5, 1)
    else:
        draw_cbutton(30, 5, 0)
    if buttons[1] == True:
        draw_zbutton(80, 5, 1)
    else:
        draw_zbutton(80, 5, 0)
    
    if not nun.joystick_center():
        if nun.joystick_up():
            draw_uparrow(48, 18, 1)
        elif nun.joystick_down():
            draw_downarrow(48, 40, 1)
        if nun.joystick_left():
            draw_leftarrow(2, 24, 1)
        elif nun.joystick_right():
            draw_rightarrow(82, 24, 1)
    else:
        draw_uparrow(48, 18, 0)
        draw_downarrow(48, 40, 0)
        draw_leftarrow(2, 24, 0)
        draw_rightarrow(82, 24, 0)
        
    
    utime.sleep_ms(3)
    
    
