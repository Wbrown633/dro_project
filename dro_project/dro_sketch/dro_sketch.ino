//This code is more general, written for Arduino (I tested it with Nano)
int dro_bits[24];        // For storing the data bit. bit_array[0] = data bit 1 (LSB), bit_array[23] = data bit 24 (MSB).
char str[7]; //Array for the char "string"

unsigned long droTimer = 0; //update frequency (the DRO is checked this often)
unsigned long buttonTimer = 0; //debouncing

int clk = 4; //Gray
int data = 5; //Brown
int button = 2;
int analog_sense = A1;

int button_counter; // 

int SERIES_RESISTOR = 560;

float convertedValue = 0.0; //raw conversion value (bit to mms)
float resultValue = 0.0; //final result value: conversion value - tare value (if there is any taring)
float previousresultValue = 0.0; //temporary storage to be able to register a change in the value
float tareValue = 0.0; //tare value to set a new zero point anywhere (using a button)
float resistance = 0.0;

float ZERO_VOLUME_RESISTANCE = 0.0; // cal value 
float CALIBRATION_RESISTANCE = 0.0; // cal value
float CALIBRATION_VOLUME = 0.0; // Volume when liquid is at max

#include <Wire.h>


void setup()
{
  Serial.begin(115200);
  Serial.println("DRO reading Arduino"); //test message to see if the serial works
  pinMode(clk, INPUT_PULLUP);
  pinMode(data, INPUT_PULLUP);
  pinMode(button, INPUT_PULLUP);
}

void loop()
{
  readEncoder();
  readButton();
}

void readButton()
{
  if (digitalRead(button) == 0)
  {
    if (millis() - buttonTimer > 300) //software "debounce"
    {
      tareValue = convertedValue; //use the most recent conversion value as the tare value
      buttonTimer = millis();
    }
  }
}

float readResistance(int pin, int seriesResistance) {
  // Get ADC value.
  float resistance = analogRead(pin);
  // Convert ADC reading to resistance.
  resistance = (1023.0 / resistance) - 1.0;
  resistance = seriesResistance / resistance;
  return resistance;
}


float resistanceToVolume(float resistance, float zeroResistance, float calResistance, float calVolume) {
  if (resistance > zeroResistance || (zeroResistance - calResistance) == 0.0) {
    // Stop if the value is above the zero threshold, or no max resistance is set (would be divide by zero).
    return 0.0;
  }
  // Compute scale factor by mapping resistance to 0...1.0+ range relative to maxResistance value.
  float scale = (zeroResistance - resistance) / (zeroResistance - calResistance);
  // Scale maxVolume based on computed scale factor.
  return calVolume * scale;
}


void readEncoder()
{
  //This function reads the encoder
  //I added a timer if you don't need high update frequency

  if (true) // removed timer because it wasn't working
  {
    convertedValue = 0; //set it to zero, so no garbage will be included in the final conversion value

    //This part was not shown in the video because I added it later based on a viewer's idea
    unsigned long syncTimer = 0; //timer for syncing the readout process with the DRO's clock signal
    bool synchronized = false; // Flag that let's the code know if the clk is synced
    while (synchronized == false)
    {
      syncTimer = millis(); //start timer
      while (digitalRead(clk) == HIGH) {} //wait until the clk goes low
      //Time between the last rising edge of CLK and the first falling edge is 115.7 ms
      //Time of the "wide high part" that separates the 4-bit parts: 410 us

      if (millis() - syncTimer > 5) //if the signal has been high for more than 5 ms, we know that it has been synced
      { //with 5 ms delay, the code can re-check the condition ~23 times so it can hit the 115.7 ms window
        synchronized = true;
      }
      else
      {
        synchronized = false;
      }
    }

    for (int i = 0; i < 23; i++) //We read the whole data block - just for consistency
    {
      while (digitalRead(clk) == LOW) {} // wait for the rising edge

      dro_bits[i] = digitalRead(data);
      //Print the data on the serial
      // Serial.print(dro_bits[i]);
      // Serial.print(" ");

      while (digitalRead(clk) == HIGH) {} // wait for the falling edge
    }
    Serial.println(" ");

    //Reconstructing the real value
    for (int i = 0; i < 20; i++) //we don't process the whole array, it is not necessary for our purpose
    {
      convertedValue = convertedValue + (pow(2, i) * dro_bits[i]);
      //Summing up all the 19 bits.
      //Essentially: 1*[i] + 2*[i] + 4*[i] + 8*[i] + 16 * [i] + ....
    }

    if (dro_bits[20] == 1)
    {
      //don't touch the value (stays positive)
      // Serial.println("Positive ");
    }
    else
    {
      convertedValue = -1 * convertedValue; // convert to negative
      // Serial.println("Negative ");
    }

    convertedValue = (convertedValue / 100.0); //conversion to mm
    //Division by 100 comes from the fact that the produced number is still an integer (e.g. 9435) and we want a float
    //The 100 is because of the resolution (0.01 mm). x/100 is the same as x*0.01.

    //The final result is stored in a separate variable where the tare is subtracted
    //We need a separate variable because the converted value changes "on its own scale".
    resultValue = convertedValue - tareValue;

    //Dump everything on the serial
    // Serial.print("Raw reading: ");
    // Serial.println(convertedValue);
    // Serial.print("Tare value: ");
    // Serial.println(tareValue);
    Serial.print("Result after taring: ");
    Serial.println(resultValue);

    resistance = readResistance(analog_sense, SERIES_RESISTOR);
    //Serial.print("Liquid sense: ");
    //Serial.println(resistance);
    // Serial.println(" ");

    droTimer = millis();
  }
}
