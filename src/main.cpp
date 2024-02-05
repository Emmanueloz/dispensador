#include <Arduino.h>
#include "ControllerDispenser.h"
#include "ControllerTimeDispenser.h"
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
const int limitWaterRecipient = 350;
const int limitWaterDispenser = 12;
const int limitFoodDispenser = 12;

// Constantes de tiempos por defecto
const long defaultTimeOpenWater = 8000;
const long defaultTimeOpenFood = 8000;

// Constantes de comandos
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "wdT";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "fdT";
const String COMMAND_WATER_DISPENSER = "wd";
const String COMMAND_FOOD_DISPENSER = "fd";

Dispensador waterDispenser;
Dispensador foodDispenser;

Sonares sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater, limitWaterDispenser);
Sonares sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood, limitFoodDispenser);

ControllerDispenser waterDispenserController(waterDispenser, sonarWater, COMMAND_WATER_DISPENSER);
ControllerDispenser foodDispenserController(foodDispenser, sonarFood, COMMAND_FOOD_DISPENSER);

void callbackWaterDispenser()
{
  int result = waterDispenser.open();
  Serial.println(COMMAND_TIME_OPEN_WATER_DISPENSER + "Task:" + result);
}

void callbackFoodDispenser()
{
  int result = foodDispenser.open();
  Serial.println(COMMAND_TIME_OPEN_FOOD_DISPENSER + "Task:" + result);
}

ControllerTimeDispenser waterDispenserTimeController(COMMAND_TIME_OPEN_WATER_DISPENSER, defaultTimeOpenWater, callbackWaterDispenser);
ControllerTimeDispenser foodDispenserTimeController(COMMAND_TIME_OPEN_FOOD_DISPENSER, defaultTimeOpenFood, callbackFoodDispenser);

void setup()
{
  Serial.begin(9600);
  waterDispenser.setup(pinWaterServo, 90, 0);
  foodDispenser.setup(pinFoodServo, 90, 0);
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
  return value.substring(index + 1);
}

void loop()
{
  /**
   * ! Evitar que se ejecute la tarea si el dispensador esta vació para evitar que el cerrado automático se active
   */
  waterDispenserTimeController.update();
  foodDispenserTimeController.update();

  waterDispenserController.closeAutomatic();
  foodDispenserController.closeAutomatic();

  if (Serial.available() > 0)
  {
    String result = Serial.readString();
    String command = getCommand(result);
    String value = getValue(result);
    // Controladores
    waterDispenserController.processCommand(command, value);
    foodDispenserController.processCommand(command, value);
    waterDispenserTimeController.processCommand(command, value);
    foodDispenserTimeController.processCommand(command, value);
  }
}
