#  *  Cooper Wutzke
#  *  Mobility Code for CW-Robot
#  *  7/26/2022
#  *  
#  *  Raspberry Pi Pico
#  *  
#  *  All Peripherals:
#  *  - L298N Motor Driver
#  *  - NRF24L01 2.4Ghz Transceiver
#  *  - 1 ADC for battery voltage monitor
#  *  - MPU6050 Accelerometer/Gyro

from machine import Pin, I2C, PWM
import time

cda = Pin(4, Pin.IN, Pin.PULL_UP)
clk = Pin(5, Pin.OUT, Pin.PULL_UP)
i2c = I2C(0)

en_a = Pin(10, Pin.OUT)
en_b = Pin(11, Pin.OUT)
in_1 = Pin(6, Pin.OUT)
in_2 = Pin(7, Pin.OUT)
in_3 = Pin(8, Pin.OUT)
in_4 = Pin(9, Pin.OUT)

l_motor_pwm = PWM(Pin(10))
l_motor_pwm.freq(1000)
r_motor_pwm = PWM(Pin(11))
r_motor_pwm.freq(1000)

def moveForward():
    in_1.value(1)
    in_2.value(0)
    in_3.value(1)
    in_4.value(0)
    
def moveBackward():
    in_1.value(0)
    in_2.value(1)
    in_3.value(0)
    in_4.value(1)
    
def spinLeft():
    in_1.value(0)
    in_2.value(1)
    in_3.value(1)
    in_4.value(0)
    
def spinRight():
    in_1.value(1)
    in_2.value(0)
    in_3.value(0)
    in_4.value(1)

def stop():
    in_1.off()
    in_2.off()
    in_3.off()
    in_4.off()

# Do Test Dance
while True:
    time.sleep(5)
    
    moveForward()
    time.sleep(2)
    stop()
    time.sleep(1)
    
    moveBackward()
    time.sleep(2)
    stop()
    time.sleep(1)
    
    spinLeft()
    time.sleep(2)
    stop()
    time.sleep(1)
    
    spinRight()
    time.sleep(2)
    stop()
    time.sleep(1)