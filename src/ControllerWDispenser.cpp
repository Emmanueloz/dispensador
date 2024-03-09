#include "ControllerWDispenser.h"

void ControllerWDispenser::setup(String command, byte pin, Sonares &sonar)
{
    sonar = sonar;
    command = command;
    pin = pin;
}

void ControllerWDispenser::processCommand(String value)
{
    if (value == "0")
    {
        if (digitalRead(pin) == HIGH)
        {
            digitalWrite(pin, LOW);
            Serial.println(command + "R:" + String(digitalRead(pin)));
        }
        else
        {
            Serial.println(command + "R:-1");
        }
    }
    else if (value == "1")
    {
        if (digitalRead(pin) == HIGH)
        {
            Serial.println(command + "R:-1");
        }
        else if (sonar.isDistanceLimit())
        {
            Serial.println(command + "R:sonarLimit");
        }
        else
        {
            digitalWrite(pin, HIGH);
            Serial.println(command + "R:" + String(digitalRead(pin)));
        }
    }
    else if (value == "2")
    {
        int result = digitalRead(pin);
        Serial.println(command + "P:" + String(result));
    }
    else
    {
        Serial.println(command + ":notFound");
    }
}
