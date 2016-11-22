//#include <SoftwareSerial.h>
#include <MsTimer2.h>

//SoftwareSerial XBee(2, 3);

#define TMP_SNS A0
#define node_id "0"

float avgTemp1 = 0.0, avgTemp2 = 0.0;
float counter1 = 0, counter2 = 0;
bool bArray = true;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(TMP_SNS, INPUT);

  MsTimer2::set(1000, getFahrenheit);
  MsTimer2::start();

  //XBee.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

  if(Serial.available())
  {
    char arg = "";

    //While there is something in the serial buffer
    //pull it out one byte at a time
    while (Serial.available())
    {
      //Read the byte
      arg = Serial.read();

      if(arg == 'R')
      {
        arg = Serial.read();

        if(arg == node_id)
        {
          bArray = !bArray;
          TxData();
        }
      }   
    }
  }
}

void TxData()
{
  //Send this shit
  if(bArray)
  {
    //Use queue2
    Serial.println(avgTemp2 / (float)counter2);
    avgTemp2 = 0;
    counter2 = 0;
    
  }else if(!bArray){
    //Use queue1
    Serial.println(avgTemp1 / (float)counter1);
    avgTemp1 = 0;
    counter1 = 0;
  }
}

void getFahrenheit()
{
  int reading = 0;

  //getting the voltage reading from the temperature sensor
  //Take 100 samples and average them to eliminate as much noise
  //as possible
  for(int i = 0; i < 100; i++)
  {
    reading += analogRead(TMP_SNS);
    delay(20);
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

  if(bArray)
  {
    avgTemp1 += temperatureF;
    counter1++;

  }else if(!bArray)
  {
    avgTemp2 += temperatureF;
    counter2++;
  }


}

