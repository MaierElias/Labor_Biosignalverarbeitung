#include <Wire.h>

#define ADS1015_ADDRESS 0x48
#define REG_CONVERSION 0x00
#define REG_CONFIG     0x01

void setup() {
  Wire.begin();
  Wire.setClock(400000);
  Serial.begin(1000000);

  // CONFIG REGISTER layout:
  // Bit15   : OS = don't care in continuous mode
  // Bits14-12: MUX = 100 for AIN0-GND
  // Bits11-9 : PGA = 001 for ±4.096V
  // Bit8    : MODE = 0 for continuous
  // Bits7-5 : DR = 111 for 3300 SPS
  // Bits4-0 : comparator disabled

  uint16_t config =
      (4 << 12) |   // MUX = AIN0-GND
      (1 << 9)  |   // Gain = ±4.096V
      (0 << 8)  |   // Continuous mode
      (7 << 5)  |   // 3300 SPS
      0x03;         // Comparator disabled

  Wire.beginTransmission(ADS1015_ADDRESS);
  Wire.write(REG_CONFIG);
  Wire.write(config >> 8);
  Wire.write(config & 0xFF);
  Wire.endTransmission();
}

void loop() {
  Wire.beginTransmission(ADS1015_ADDRESS);
  Wire.write(REG_CONVERSION);
  Wire.endTransmission();

  Wire.requestFrom(ADS1015_ADDRESS, 2);
  if (Wire.available() == 2) {
    uint16_t raw = (Wire.read() << 8) | Wire.read();
    raw >>= 4;  // ADS1015 left-aligns 12-bit results
    Serial.println(raw);
  }
}
