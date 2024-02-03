#include <Arduino.h>
#include <Servo.h>
#include <NewPing.h>
#include "Dispensador.h"
// Pines
const byte pinLevelWater = A15; // Replace A15 with the corresponding pin number

const byte pinWaterServo = 13;
const byte pinFoodServo = 12;

const int pinEchoWater = 10;
const int pinTriggerWater = 9;

const int pinEchoFood = 6;
const int pinTriggerFood = 5;

// pin de los botones
const byte pinButtonWater = 2;
const byte pinButtonFood = 3;
// Constantes enteras
const int maxSonarWater = 400;
const int maxSonarFood = 400;
const int timeOpenFood = 5000;
const int limitlWaterRecipient = 350;
const int limitWaterDispenser = 12;
const int limitFoodDispenser = 12;
const int delayInfo = 2000;
const int delayWarning = 150;
// Constantes de comandos
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "timeOWD";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "timeOFD";
const String COMMAND_OPEN_WATER_DISPENSER = "openWD";
const String COMMAND_OPEN_FOOD_DISPENSER = "openFD";
enum STATES
{
  CLOSE,
  OPEN
};
STATES stateWaterDispenser = CLOSE;
STATES stateFoodDispenser = CLOSE;

// Servos
// Servo waterServo;
// Servo foodServo;

Dispensador waterDispenser;
Dispensador foodDispenser;

// Ultrasonicos
NewPing sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater);
NewPing sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood);

void setup()
{
  Serial.begin(9600);
  waterDispenser.setup(pinWaterServo, 90, 0);
}

void loop()
{
  if (Serial.available() > 0)
  {
    String command = Serial.readString();
    if (command == "1")
    {
      int result = waterDispenser.open();
      Serial.println(result == 90 ? "1" : "No");
    }
    else if (command == "2")
    {
      int result = waterDispenser.close();
      Serial.println(result == 0 ? "0" : "No");
    }
    else if (command == "3")
    {
      int result = waterDispenser.getPosition();
      Serial.println(result == 90 ? "1" : "0");
    }
  }
}