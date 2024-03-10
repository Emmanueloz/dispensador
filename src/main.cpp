#include <Arduino.h>

#include "ControllerTimeDispenser.h"
#include "ControllerSonar.h"

#include "ControllerWDispenser.h"
#include "ControllerFDispenser.h"
// Pines
const byte pinLevelWater = A15;

const byte pinWaterServo = 13;
const byte pinFoodServo = 12;

const byte pinEchoWater = 10;
const byte pinTriggerWater = 9;
const byte pinEchoFood = 7;
const byte pinTriggerFood = 6;

const byte pinEchoFoodLevel = 5;
const byte pinTriggerFoodLevel = 4;

// Constantes enteras
const int maxSonarWater = 400;
const int maxSonarFood = 400;

const int limitWaterRecipient = 350;

const int limitWaterDispenser = 20;

const int limitFoodRecipient = 1;
const int limitFoodDispenser = 25;

// Constantes de tiempos por defecto
const long defaultTimeOpenWater = 3600000;
const long defaultTimeOpenFood = 3600000;

// Constantes de comandos
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "wdT";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "fdT";
const String COMMAND_WATER_DISPENSER = "wd";
const String COMMAND_FOOD_DISPENSER = "fd";
const String COMMAND_WATER_LEVEL = "wdS";
const String COMMAND_FOOD_LEVEL = "fdS";

const String COMMAND_ALL_STATUS = "all";

Sonares sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater, limitWaterDispenser);
Sonares sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood, limitFoodDispenser);

Sonares sonarFoodLevel(pinTriggerFoodLevel, pinEchoFoodLevel, maxSonarFood, limitFoodRecipient);

ControllerWDispenser waterDispenserController(sonarWater, COMMAND_WATER_DISPENSER, pinLevelWater, limitWaterRecipient);
ControllerFDispenser foodDispenserController(sonarFood, COMMAND_FOOD_DISPENSER, sonarFoodLevel);

ControllerSonar sonarWaterController(sonarWater, COMMAND_WATER_LEVEL);
ControllerSonar sonarFoodController(sonarFood, COMMAND_FOOD_LEVEL);

void callbackWaterDispenser()
{

  const int result = waterDispenserController.open();
  Serial.println(COMMAND_TIME_OPEN_WATER_DISPENSER + "R:" + String(result));
}

void callbackFoodDispenser()
{

  const int result = foodDispenserController.open();
  Serial.println(COMMAND_TIME_OPEN_FOOD_DISPENSER + "R:" + String(result));
}

ControllerTimeDispenser waterDispenserTimeController(COMMAND_TIME_OPEN_WATER_DISPENSER, defaultTimeOpenWater, 'm', callbackWaterDispenser);
ControllerTimeDispenser foodDispenserTimeController(COMMAND_TIME_OPEN_FOOD_DISPENSER, defaultTimeOpenFood, 'm', callbackFoodDispenser);

void setup()
{
  Serial.begin(9600);
  waterDispenserController.setup(pinWaterServo);
  foodDispenserController.setup(pinFoodServo, 90, 0);
  waterDispenserTimeController.start();
  foodDispenserTimeController.start();
}

String getCommand(String value)
{
  int index = value.indexOf(":");
  return value.substring(0, index);
}

String getValue(String value)
{
  int index = value.indexOf(":");
  String resul = value.substring(index + 1);
  resul.trim();
  return resul;
}

void loop()
{
  waterDispenserController.closeAutomatic();
  foodDispenserController.closeAutomatic();

  waterDispenserTimeController.update();
  foodDispenserTimeController.update();

  if (Serial.available() > 0)
  {
    String result = Serial.readString();
    String command = getCommand(result);
    String value = getValue(result);
    // # Controladores

    if (command == COMMAND_WATER_DISPENSER)
    {
      waterDispenserController.processCommand(value);
    }
    else if (command == COMMAND_FOOD_DISPENSER)
    {
      foodDispenserController.processCommand(value);
    }
    else if (command == COMMAND_TIME_OPEN_WATER_DISPENSER)
    {
      waterDispenserTimeController.processCommand(value);
    }
    else if (command == COMMAND_TIME_OPEN_FOOD_DISPENSER)
    {
      foodDispenserTimeController.processCommand(value);
    }
    else if (command == COMMAND_WATER_LEVEL)
    {
      sonarWaterController.processCommand(value);
    }
    else if (command == COMMAND_FOOD_LEVEL)
    {
      sonarFoodController.processCommand(value);
    }
    else if (command == COMMAND_ALL_STATUS)
    {
      const String estadoWD = String(waterDispenserController.isOpen());
      const String estadoFD = String(foodDispenserController.isOpen());
      const String estadoWL = String(sonarWater.isDistanceLimit());
      const String estadoFL = String(sonarFood.isDistanceLimit());

      const String estadoWTD = String(waterDispenserTimeController.getTimer());
      const String estadoFTD = String(foodDispenserTimeController.getTimer());

      Serial.println(estadoWD + "," + estadoFD + "," + estadoWL + "," + estadoFL + "," + estadoWTD + "," + estadoFTD);
    }
  }
}
