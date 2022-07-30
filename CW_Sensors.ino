/* 
 *  Cooper Wutzke
 *  Sensor Suite Test for CW-Robot
 *  7/26/2022
 *  
 *  AI-Thinker ESP32-CAM
 *  
 *  All Peripherals:
 *  - *Testing* SSD1306 Oled 0.96in Display
 *  - NEO-6M GPS Module
 *  - DHT-22 Temp/Humidity Sensor
 *  - L298N Motor Driver
 *  - 1 ADC for battery voltage monitor
 */

#include <Wire.h>
#include <TinyGPSPlus.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define RX_PIN 12
#define TX_PIN 13
#define CDA_PIN 15
#define CLK_PIN 14
#define BAT_ADC 16
#define EN_A 4
#define EN_B 2
#define IN_1 0
#define IN_2 0
#define IN_3 0
#define IN_4 0

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_MPU6050 mpu;
TinyGPSPlus gps;
HardwareSerial GpsSerial(2);
 
void setup() {
  // Pin 15 = Data | Pin 14 = Clk
  Wire.begin(CDA_PIN, CLK_PIN);
  GpsSerial.begin(9600, RX_PIN, TX_PIN);
  Serial.begin(115200);
  Serial.println("\nSensor Suite");

  checkDevices();
  display.clearDisplay();
  display.print("***************");
  display.print("*     GPS     *");
  display.print("*     MPU     *");
  display.print("*     BAT     *");
  display.print("***************");
  delay(5000);
  display.clearDisplay();
  display.setTextColor(WHITE);
}
 
void loop() {   
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  // READ GPS
  //readGps();

  // PRINT AND DISPLAY MPU VALUES
  //readMpu();
  readSensors();
  display.display();
  display.clearDisplay();
  smartDelay(3000);         
}

static void checkDevices()
{
  byte error, address;
  int nDevices;
  
  // I2C SCANNING LOOP
  nDevices = 0;
  for(address = 1; address < 127; address++) 
  {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) 
    {
      Serial.print("I2C device found at address 0x");
      if (address<16) 
      {
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) 
    {
      Serial.print("Unknow error at address 0x");
      if (address<16) 
      {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0) 
  {
    Serial.println("No I2C devices found\n");
  }
  else 
  {
    Serial.println("done\n");
  }
  smartDelay(1000);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) 
  {
    Serial.println(F("SSD1306 allocation failed"));
  }

  if (!mpu.begin()) 
  {
    Serial.println("Failed to find MPU6050 chip");
  }
  Serial.println("MPU6050 Found!");
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

static void readMpu()
{  
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // PRINT AND DISPLAY MPU VALUE
  display.setCursor(0, 26);

  /*
  Serial.print("Accelerometer ");
  Serial.print("X: ");
  Serial.print(a.acceleration.x, 1);
  Serial.print(" m/s^2, ");
  Serial.print("Y: ");
  Serial.print(a.acceleration.y, 1);
  Serial.print(" m/s^2, ");
  Serial.print("Z: ");
  Serial.print(a.acceleration.z, 1);
  Serial.println(" m/s^2"); */

  display.println("Accel - m/s^2");
  display.print(a.acceleration.x, 1);
  display.print(", ");
  display.print(a.acceleration.y, 1);
  display.print(", ");
  display.print(a.acceleration.z, 1);
  display.println("");

  /*
  Serial.print("Gyroscope ");
  Serial.print("X: ");
  Serial.print(g.gyro.x, 1);
  Serial.print(" rps, ");
  Serial.print("Y: ");
  Serial.print(g.gyro.y, 1);
  Serial.print(" rps, ");
  Serial.print("Z: ");
  Serial.print(g.gyro.z, 1);
  Serial.println(" rps"); */

  display.println("Gyroscope - rps");
  display.print(g.gyro.x, 1);
  display.print(", ");
  display.print(g.gyro.y, 1);
  display.print(", ");
  display.print(g.gyro.z, 1);
  display.println("");

  display.display(); 
}

static void readGps()
{
  display.setCursor(0, 0);

  display.print("GPS Data - ");
  display.print(gps.date.value());
  display.print("\n");
  display.print(gps.time.hour());
  display.print(":");
  display.print(gps.time.minute());
  display.print("| Sat# ");
  display.print(gps.satellites.value());
  display.print(" La ");
  display.print(gps.location.lat());
  display.print(" Ln ");
  display.print(gps.location.lng());

  display.display();
 
  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("No GPS data received: check wiring"));
}

static void readSensors()
{
  display.setCursor(0, 0);

  display.print("GPS Data - ");
  display.print(gps.date.value());
  display.print("\n");
  display.print(gps.time.hour());
  display.print(":");
  display.print(gps.time.minute());
  display.print("| Sat# ");
  display.print(gps.satellites.value());
  display.print(" La ");
  display.print(gps.location.lat());
  display.print(" Ln ");
  display.print(gps.location.lng());

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // PRINT AND DISPLAY MPU VALUE
  display.setCursor(0, 26);

  display.println("Accel - m/s^2");
  display.print(a.acceleration.x, 1);
  display.print(", ");
  display.print(a.acceleration.y, 1);
  display.print(", ");
  display.print(a.acceleration.z, 1);
  display.println("");

  display.println("Gyroscope - rps");
  display.print(g.gyro.x, 1);
  display.print(", ");
  display.print(g.gyro.y, 1);
  display.print(", ");
  display.print(g.gyro.z, 1);
  display.println("");

  display.display();
}



// This custom version of delay() ensures that the gps object
// is being "fed".
static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (GpsSerial.available())
      gps.encode(GpsSerial.read());
  } while (millis() - start < ms);
}
