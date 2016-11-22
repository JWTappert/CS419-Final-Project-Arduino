#include <SoftwareSerial.h>
#include <MsTimer2.h>

SoftwareSerial XBee(2, 3);

#define aref_voltage 3.3

#define TMP_SNS A0

float avgTemp = 0.0;
short counter = 0;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(TMP_SNS, INPUT);

  MsTimer2::set(1000, getFahrenheit);
  MsTimer2::start();

  // If you want to set the aref to something other than 5v
  //analogReference(EXTERNAL);

  XBee.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
}

float readTemp()
{
  long rd = 0;

  for(short i = 0; i < 10; i++)
  {
    rd += analogRead(TMP_SNS);
    delay(20);
  }
  return rd/10.0;
}

float getVoltage()
{
    return (readTemp() * 5.0) / 1024.0;
}

float getCelsius()
{
    return (getVoltage() - 0.5) / 100.0;
}

float getFahrenheit()
{
  int reading = 0;

  //getting the voltage reading from the temperature sensor
  //Take 100 samples and average them to eliminate as much noise
  //as possible
  for(int i = 0; i < 100; i++)
  {
    reading += analogRead(TMP_SNS);
  }
  reading /= 100.0;
 
  // converting that reading to voltage
  float voltage = reading * 5.0;
  voltage /= 1024.0; 
 
  // print out the voltage, for testing
  Serial.print(voltage); Serial.println(" volts");
 
  // now print out the temperature in Celcius, for testing
  float temperatureC = (voltage - 0.5) * 100 ;
  Serial.print(temperatureC); Serial.println(" degrees C");
 
  // now convert to Fahrenheit
  float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
  Serial.print(temperatureF); Serial.println(" degrees F");

  avgTemp += temperatureF;
  counter++;

  if(counter == 60)
  {
    Serial.print("THIS IS THE AVG: ");
    Serial.println(avgTemp / 60.0);
    avgTemp = 0;
    counter = 0;
  }
    /*float temp = (getCelsius() * 9.0/5.0) + 32.0;
    Serial.println(temp);
    avgTemp += temp;
    counter++;

    if(counter == 9)
    {
      counter = 0;
      Serial.println(avgTemp / 10.000);
      avgTemp = 0;
    }*/
    return temperatureF;
}

