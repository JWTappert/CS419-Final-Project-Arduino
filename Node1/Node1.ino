#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3);


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  XBee.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

  delay(500);
  XBee.print("A");
  Serial.println("B");

}
