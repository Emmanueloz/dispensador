#include <Arduino.h>
#include "ControllerDispenser.h"
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
const int limitWaterRecipient = 350;
const int limitWaterDispenser = 12;
const int limitFoodDispenser = 12;
const int delayInfo = 2000;
const int delayWarning = 150;
// Constantes de comandos
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "timeOWD";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "timeOFD";
const String COMMAND_WATER_DISPENSER = "wd";
const String COMMAND_FOOD_DISPENSER = "fd";

Dispensador waterDispenser;
Dispensador foodDispenser;

Sonares sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater, limitWaterDispenser);
Sonares sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood, limitFoodDispenser);

ControllerDispenser waterDispenserController(waterDispenser, sonarWater, COMMAND_WATER_DISPENSER);
ControllerDispenser foodDispenserController(foodDispenser, sonarFood, COMMAND_FOOD_DISPENSER);

void setup()
{
  Serial.begin(9600);
  waterDispenser.setup(pinWaterServo, 90, 0);
  foodDispenser.setup(pinFoodServo, 90, 0);
}

String getCommand(String value)
{
  int index = value.indexOf(":");
  return value.substring(0, index);
}

String getValue(String value)
{
  int index = value.indexOf(":");
  return value.substring(index + 1);
}

void loop()
{
  if (Serial.available() > 0)
  {
    String result = Serial.readString();
    String command = getCommand(result);
    String value = getValue(result);

    waterDispenserController.processCommand(command, value);
    foodDispenserController.processCommand(command, value);
  }

  waterDispenserController.closeAutomatic();
  foodDispenserController.closeAutomatic();
}
