#include <Arduino.h>
#include <Servo.h>
#include <NewPing.h>
// Pines
const byte pinLevelWater = A15; // Replace A15 with the corresponding pin number

const byte pinWaterServo = 13;
const byte pinFoodServo = 12;

const int pinEchoWater = 10;
const int pinTriggerWater = 9;

const int pinEchoFood = 6;
const int pinTriggerFood = 5;

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
const String COMMAND_TIME_OPEN_WATER_DISPENSER = "timeOpenWaterDispenser";
const String COMMAND_TIME_OPEN_FOOD_DISPENSER = "timeOpenFoodDispenser";
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
Servo waterServo;
Servo foodServo;
// Ultrasonicos
NewPing sonarWater(pinTriggerWater, pinEchoWater, maxSonarWater);
NewPing sonarFood(pinTriggerFood, pinEchoFood, maxSonarFood);

// Valores
int waterLevel;
int dcWaterDispenser;
int dcFoodDispenser;

bool buttonWater = LOW;
bool buttonFood = LOW;
// int stateButtonWater = LOW;
// int stateButtonFood = LOW;

// Variable de tiempo
int delayAutomaticWaterDispenser = 10000;
int delayAutomaticFoodDispenser = 10000;
unsigned long timeAutomaticDelayOpensWaterDispenser = millis() + delayAutomaticWaterDispenser;
unsigned long timeAutomaticDelayOpensFoodDispenser = millis() + delayAutomaticFoodDispenser;
unsigned long timeAutomaticDelayCloseFoodDispenser;
unsigned long timeDelayInfo = millis() + delayInfo;
unsigned long timeDelayWarningWater = millis() + delayWarning;
unsigned long timeDelayWarningFood = millis() + delayWarning;
unsigned long timeDelayButtonWater = millis() + delayWarning;
unsigned long timeDelayButtonFood = millis() + delayWarning;

void setup()
{
  Serial.begin(9600);
  waterServo.attach(pinWaterServo);
  foodServo.attach(pinFoodServo);
  waterServo.write(0);
  foodServo.write(90);
  pinMode(pinButtonWater, INPUT);
  pinMode(pinButtonFood, INPUT);
}

void loop()
{
  waterLevel = analogRead(pinLevelWater);
  dcWaterDispenser = sonarWater.ping_cm();
  dcFoodDispenser = sonarFood.ping_cm();
  readCommandos();
  printInfo();
  printWarning();
  listenButtonActions();
  openAutomaticDispenser();
  closeAutomaticDispense();
}

void closeAutomaticDispense()
{
  if (stateWaterDispenser == OPEN && waterLevel > limitlWaterRecipient)
  {
    Serial.println("Cerrar el dispensador de agua automatico");
    stateWaterDispenser = CLOSE;
    Serial.println("");
    actionServoWater(CLOSE);
    timeAutomaticDelayOpensWaterDispenser = millis() + delayAutomaticWaterDispenser;
  }
  if (stateFoodDispenser == OPEN && millis() > timeAutomaticDelayCloseFoodDispenser)
  {
    Serial.println("Cerrar el dispensador de alimento automatico");
    stateFoodDispenser = CLOSE;
    actionServoFood(CLOSE);
    timeAutomaticDelayOpensFoodDispenser = millis() + delayAutomaticFoodDispenser;
  }
}

void openAutomaticDispenser()
{
  if (millis() > timeAutomaticDelayOpensWaterDispenser)
  {
    openWaterDispenser("Servir dispensador de agua automatico");
    timeAutomaticDelayOpensWaterDispenser = millis() + delayAutomaticWaterDispenser;
  }
  if (millis() > timeAutomaticDelayOpensFoodDispenser)
  {
    Serial.println();
    openFoodDispenser("Servir dispensador de alimento automatico");
    timeAutomaticDelayOpensFoodDispenser = millis() + delayAutomaticFoodDispenser;
  }

  if (millis() > timeAutomaticDelayOpensWaterDispenser && stateWaterDispenser == CLOSE)
  {
    timeAutomaticDelayOpensWaterDispenser = millis() + delayAutomaticWaterDispenser;
  }
}

void openWaterDispenser(String msg)
{
  if (stateWaterDispenser == CLOSE && waterLevel < limitlWaterRecipient)
  {
    Serial.println(msg);
    stateWaterDispenser = OPEN;
    actionServoWater(OPEN);
  }
}

void openFoodDispenser(String msg)
{
  if (stateFoodDispenser == CLOSE)
  {
    Serial.println(msg);
    stateFoodDispenser = OPEN;
    timeAutomaticDelayCloseFoodDispenser = millis() + timeOpenFood;
    actionServoFood(OPEN);
  }
}

void listenButtonActions()
{

  buttonWater = digitalRead(pinButtonWater);
  buttonFood = digitalRead(pinButtonFood);
  waterLevel = analogRead(pinLevelWater);

  if (buttonWater == HIGH && stateWaterDispenser == CLOSE && waterLevel < limitlWaterRecipient)
  {
    Serial.println("Servir agua boton");
    Serial.println(buttonWater);
    stateWaterDispenser = OPEN;
    actionServoWater(OPEN);
  }
  if (buttonFood == HIGH && stateFoodDispenser == CLOSE)
  {
    Serial.println("Servir alimento boton");
    Serial.println(buttonFood);
    stateFoodDispenser = OPEN;
    timeAutomaticDelayCloseFoodDispenser = millis() + timeOpenFood;
    actionServoFood(OPEN);
  }
}

void printWarning()
{
  if (dcWaterDispenser > limitWaterDispenser)
  {
    if (millis() > timeDelayWarningWater)
    {
      Serial.println("dispensador de agua esta vacio");
      timeDelayWarningWater = millis() + delayWarning;
    }
  }
  if (dcFoodDispenser > limitFoodDispenser)
  {
    if (millis() > timeDelayWarningFood)
    {
      Serial.println("dispensador de alimento esta vacio");
      timeDelayWarningFood = millis() + delayWarning;
    }
  }
}

void printInfo()
{
  if (millis() > timeDelayInfo)
  {
    Serial.println("#Info de los sensores#");
    Serial.println("DC vacio DISP agua " + String(dcWaterDispenser));
    Serial.println("DC vacio DISP alimento " + String(dcFoodDispenser));
    Serial.println("Nivel agua traste " + String(waterLevel));
    Serial.println("Estado DISP agua " + String(stateWaterDispenser));
    Serial.println("Estado DISP alimento " + String(stateFoodDispenser));
    timeDelayInfo = millis() + delayInfo;
  }
}

void readCommandos()
{
  if (Serial.available() > 0)
  {
    // Lee una línea completa desde el monitor serial
    String input = Serial.readStringUntil('\n');
    // Verifica si la línea no está vacía
    if (input.length() > 0)
    {
      // Encuentra la posición del carácter ':' en la cadena
      int separatorIndex = input.indexOf(':');

      // Verifica si se encontró el carácter ':'
      if (separatorIndex != -1)
      {
        // Extrae el comando y el valor de la cadena
        String command = input.substring(0, separatorIndex);
        String valueString = input.substring(separatorIndex + 1);

        // Convierte el valor a un número entero
        int value = valueString.toInt();

        if (value >= 0)
        {
          // Realiza acciones basadas en el comando
          if (command.equals(COMMAND_TIME_OPEN_WATER_DISPENSER) && value >= 0)
          {
            // Realiza acciones para el comando timeOpenWaterDispenser
            Serial.print("Comando: " + COMMAND_TIME_OPEN_WATER_DISPENSER + " Valor: ");
            Serial.println(value);
            delayAutomaticWaterDispenser = value;
            timeAutomaticDelayOpensWaterDispenser = millis() + value;
            Serial.println("Milisegundo para abrir el dis agua");
            Serial.println(timeAutomaticDelayOpensWaterDispenser);
          }
          else if (command.equals(COMMAND_TIME_OPEN_FOOD_DISPENSER) && value >= 0)
          {
            // Realiza acciones para el comando timeOpenFoodDispenser
            Serial.print("Comando: " + COMMAND_TIME_OPEN_FOOD_DISPENSER + " Valor: ");
            Serial.println(value);
            delayAutomaticFoodDispenser = value;
            timeAutomaticDelayOpensFoodDispenser = millis() + value;
            Serial.println("Milisegundo para abrir el dis alimento");
            Serial.println(timeAutomaticDelayOpensFoodDispenser);
          }
          else if (command.equals(COMMAND_OPEN_WATER_DISPENSER) && value == 1)
          {
            Serial.println("Comando: " + COMMAND_OPEN_WATER_DISPENSER + " Valor: " + value);
            openWaterDispenser("Servir dispensador de agua por comando");
          }
          else if (command.equals(COMMAND_OPEN_FOOD_DISPENSER))
          {
            Serial.println("Comando: " + COMMAND_OPEN_FOOD_DISPENSER + " Valor: " + value);
            openWaterDispenser("Servir dispensador de alimento por comando");
          }
          else
          {
            // Comando desconocido
            Serial.println("Comando desconocido");
          }
        }
        else
        {
          Serial.println("Valor fuera de rango, debe ser menor a 32767");
        }
      }
      else
      {
        // No se encontró el carácter ':'
        Serial.println("Formato incorrecto. Se espera comando:valor");
      }
    }
  }
}

void actionServoWater(STATES action)
{
  int degrees = action == OPEN ? 90 : 0;
  waterServo.write(degrees);
}

void actionServoFood(STATES action)
{
  int degrees = action == OPEN ? 0 : 90;
  foodServo.write(degrees);
}