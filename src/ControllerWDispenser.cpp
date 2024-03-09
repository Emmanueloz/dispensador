#include "ControllerWDispenser.h"

ControllerWDispenser::ControllerWDispenser(Sonares &sonar, String command, byte pinLevelWater, int limitWaterRecipient) : sonar(sonar)
{
    command = command;
    pinLevelWater = pinLevelWater;
    limitWaterRecipient = limitWaterRecipient;
}

void ControllerWDispenser::setup(byte pin)
{
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    pin = pin;
}

int ControllerWDispenser::open()
{
    if (isOpen())
    {
        return -1;
    }
    else if (sonar.isDistanceLimit())
    {
        return -2;
    }
    else if (analogRead(pinLevelWater) > limitWaterRecipient)
    {
        return -3;
    }

    digitalWrite(pin, HIGH);
    return digitalRead(pin);
}

int ControllerWDispenser::close()
{
    if (!isOpen())
    {
        return -1;
    }

    digitalWrite(pin, LOW);
    return digitalRead(pin);
}

bool ControllerWDispenser::isOpen()
{
    const int result = digitalRead(pin);
    return result == HIGH;
}

void ControllerWDispenser::processCommand(String value)
{
    if (value == "0")
    {
        const int result = close();
        Serial.println(command + "R:" + String(result));
    }
    else if (value == "1")
    {
        const int result = open();
        Serial.println(command + "R:" + String(result));
    }
    else if (value == "2")
    {
        const bool result = isOpen();
        Serial.println(command + "P:" + String(result));
    }
    else
    {
        Serial.println(command + ":notFound");
    }
}

void ControllerWDispenser::closeAutomatic()
{
    if (sonar.isDistanceLimit() && isOpen())
    {
        const int result = close();
        Serial.println(command + "A:Con" + String(result));
    }
    else if (analogRead(pinLevelWater) > limitWaterRecipient && isOpen())
    {
        const int result = close();
        Serial.println(command + "A:Res" + String(result));
    }
}
