#include "SparkFun_Si7021_Breakout_Library.h"

#define node_id '0'

float avgTemp1 = 0.0, avgTemp2 = 0.0;
float counter1 = 0, counter2 = 0;
bool bArray = true, bReady = false;

int power = A3;
int GND = A2;

unsigned long lastReading = 0;

//Create Instance of HTU21D or SI7021 temp and humidity sensor and MPL3115A2 barrometric sensor
Weather sensor;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  pinMode(power, OUTPUT);
  pinMode(GND, OUTPUT);

  digitalWrite(power, HIGH);
  digitalWrite(GND, LOW);

  //Initialize the I2C sensors and ping them
  sensor.begin();
}

void loop() {

  //When the base station broadcasts data
  if(Serial.available())
  {
    char arg = "";

    //While there is something in the serial buffer
    //pull it out one byte at a time
    while (Serial.available())
    {
      //Read the byte
      arg = Serial.read();

      //THe master will broadcast an R when it's Request data from a node
      if(arg == node_id)
      {
        //Serial.print("R recieved");
        //arg = Serial.read();

        //The R will be followed with the node it is requesting data from
        //if(arg == node_id)
        //{
          //Serial.print("0 processed");
          //Throw away data recorded from last request
          if(bArray)
          {
            avgTemp2 = 0;
            counter2 = 0;
          }else if(!bArray){
            avgTemp1 = 0;
            counter1 = 0;
          }

          //Switch what variables we will use to record data on next period
          bArray = !bArray;
          TxData(); //Send data
        //}
        
      }else if(arg == 'S'){ //Start recording data
        //Serial.print("S recieved");
        bReady = true;   
      }else if(arg == 'T'){ //Stop recording data
        //Serial.print("T recieved");
        bReady = false;
      }else if(arg == 'E'){ //Retransmission request

        arg = Serial.read();

        //Make sure retransmission is for this node
        if(arg == node_id)
        {
          Retransmit(); //Send data
        }
      }
    }
  }

  //If we have been told to start recording data...
  if(bReady)
  {
    //Every 1 second...
    if(millis() - lastReading >= 1000)
    {
      float temp = 0;

      //Get the current temperature
      temp = sensor.getTempF();

      //Serial.print(temp);
      
      //Update time of last reading
      lastReading = millis();

      //Store data in appropriate variables
      if(bArray)
      {
        avgTemp1 += temp;
        counter1++;
      }else if(!bArray){
  
        avgTemp2 += temp;
        counter2++;
      }
    }
  }
}

void Retransmit()
{
  //Send this shit
  //With opposite logic from TxData()
  if(!bArray)
  {
    //Use queue2
    Serial.println(avgTemp2 / (float)counter2);
  }else if(bArray){
    //Use queue1
    Serial.println(avgTemp1 / (float)counter1);
  }
  
}

void TxData()
{
  //Serial.println("Tx'n");
  //Send this shit
  if(bArray)
  {
    //Use queue2
    Serial.println(avgTemp2 / (float)counter2);
  }else if(!bArray){
    //Use queue1
    Serial.println(avgTemp1 / (float)counter1);
  }
}

