#include <SoftwareSerial.h>

char ssid[] = "NETGEAR63";
char pass[] = "crispymint130";

const byte XB_RX = 2;
const byte XB_TX = 3;

SoftwareSerial xB(XB_RX, XB_TX);
const int XBEE_BAUD = 9600;

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  while(!Serial){
    ;
  }

  xB.begin(XBEE_BAUD);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  delay(500);
  xB.print("A");
  Serial.println("B");

}
