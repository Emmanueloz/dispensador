#include <Arduino.h>
#include "ControllerDispenser.h"
#include "ControllerTimeDispenser.h"
#include "ControllerSonar.h"
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

// pin de los botones
const byte pinButtonWater = 2;
const byte pinButtonFood = 3;

// Constantes enteras
const int maxSonarWater = 400;
const int maxSonarFood = 400;
const int limitWaterRecipient = 350;
const int limitWaterDispenser = 40;
const int limitFoodRecipient = 40;
const int limitFoodDispenser = 40;

// Constantes de tiempos por defecto
const long defaultTimeOpenWater = 4000;
const long defaultTimeOpenFood = 4000;

// Constantes de comandos
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "wdT";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "fdT";
const String COMMAND_WATER_DISPENSER = "wd";
const String COMMAND_FOOD_DISPENSER = "fd";
const String COMMAND_WATER_LEVEL = "wdR";
const String COMMAND_FOOD_LEVEL = "fdR";

Dispensador waterDispenser;
Dispensador foodDispenser;

Sonares sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater, limitWaterDispenser);
Sonares sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood, limitFoodDispenser);

Sonares sonarFoodLevel(pinTriggerFoodLevel, pinEchoFoodLevel, maxSonarFood, limitFoodRecipient);

ControllerDispenser waterDispenserController(waterDispenser, sonarWater, COMMAND_WATER_DISPENSER, pinButtonWater);
ControllerDispenser foodDispenserController(foodDispenser, sonarFood, COMMAND_FOOD_DISPENSER, pinButtonFood);

ControllerSonar sonarWaterController(sonarWater, COMMAND_WATER_LEVEL);
ControllerSonar sonarFoodController(sonarFood, COMMAND_FOOD_LEVEL);

void callbackWaterDispenser()
{
  if (!waterDispenser.isOpen() && !sonarWater.isDistanceLimit())
  {
    int result = waterDispenser.open();
    Serial.println(COMMAND_TIME_OPEN_WATER_DISPENSER + "result:" + result);
  }
}

void callbackFoodDispenser()
{
  if (!foodDispenser.isOpen() && !sonarFood.isDistanceLimit())
  {
    int result = foodDispenser.open();
    Serial.println(COMMAND_TIME_OPEN_FOOD_DISPENSER + "result:" + result);
  }
}

ControllerTimeDispenser waterDispenserTimeController(COMMAND_TIME_OPEN_WATER_DISPENSER, defaultTimeOpenWater, 's', callbackWaterDispenser);
ControllerTimeDispenser foodDispenserTimeController(COMMAND_TIME_OPEN_FOOD_DISPENSER, defaultTimeOpenFood, 's', callbackFoodDispenser);

void setup()
{
  Serial.begin(9600);
  waterDispenser.setup(pinWaterServo, 90, 0);
  foodDispenser.setup(pinFoodServo, 90, 0);
  waterDispenserTimeController.start();
  foodDispenserTimeController.start();
  pinMode(pinButtonWater, INPUT);
  pinMode(pinButtonFood, INPUT);
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
  waterDispenserController.closeAutomatic();
  foodDispenserController.closeAutomatic();

  if (foodDispenser.isOpen() && !sonarFoodLevel.isDistanceLimit())
  {
    foodDispenser.close();
  }

  if (waterDispenser.isOpen() && analogRead(pinLevelWater) > limitWaterRecipient)
  {
    waterDispenser.close();
  }

  waterDispenserTimeController.update();
  foodDispenserTimeController.update();

  waterDispenserController.listenButton();
  foodDispenserController.listenButton();

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
  }
}
