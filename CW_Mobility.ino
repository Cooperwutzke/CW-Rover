/* 
 *  Cooper Wutzke
 *  Mobility Code for CW-Robot
 *  7/26/2022
 *  
 *  Raspberry Pi Pico
 *  
 *  All Peripherals:
 *  - Wii Nunchuck for input
 *  - L298N Motor Driver
 *  - 1 ADC for battery voltage monitor
 *  - MPU6050 Accelerometer/Gyro
 */

#include <Wire.h>
#include <WiiChuck.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

#define CLK_PIN 0
#define CDA_PIN 0
#define BAT_ADC 0

#define EN_A 4
#define EN_B 2
#define IN_1 0
#define IN_2 0
#define IN_3 0
#define IN_4 0

Adafruit_MPU6050 mpu;
Accessory nunchuck1;

void setup() 
{
  Wire.begin(CDA_PIN, CLK_PIN);
  Serial.begin(115200);

  if (nunchuck1.type == Unknown)
  {
    nunchuck1.type = NUNCHUCK;
  }
}

void loop() 
{
  nunchuck1.readData();    // Read inputs and update maps
  nunchuck1.printInputs(); // Print all inputs
  for (int i = 0; i < WII_VALUES_ARRAY_SIZE; i++) 
  {
    Serial.println(
        "Controller Val " + String(i) + " = "
            + String((uint8_t) nunchuck1.values[i]));
  }
}
