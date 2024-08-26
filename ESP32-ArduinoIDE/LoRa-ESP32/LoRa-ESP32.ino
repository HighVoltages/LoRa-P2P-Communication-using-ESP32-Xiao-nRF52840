// Include the necessary library
#include <HardwareSerial.h>

// Create an instance of HardwareSerial
HardwareSerial ReyaxLoRaSerial(1); 

void setup() {
  // Initialize the primary hardware serial port for monitoring
  Serial.begin(115200);
  Serial.println();
  delay(2000);

  // Initialize the secondary hardware serial port for communication with Reyax LoRa
  // Parameters are (TX pin, RX pin)
  ReyaxLoRaSerial.begin(9600, SERIAL_8N1, 4, 5); // Change 4 and 5 to the pins you want to use

  delay(1000);

  Serial.println();
  Serial.println("Serial monitor settings :");
  Serial.println("- End Char  : Newline");
  Serial.println("- Baud Rate : 115200");
  Serial.println();
}

void loop() { 
  // Read data from ReyaxLoRa and send it to Serial monitor
  if (ReyaxLoRaSerial.available()) {
    Serial.println(ReyaxLoRaSerial.readString());
  }
  
  // Read data from Serial monitor and send it to ReyaxLoRa
  if (Serial.available()) {
    ReyaxLoRaSerial.print(Serial.readString());
  }
}
