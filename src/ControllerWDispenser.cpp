#include "ControllerWDispenser.h"

ControllerWDispenser::ControllerWDispenser(Sonares &sonar, String command, byte pinLevelWater, int limitWaterRecipient) : sonar(sonar)
{
    this->command = command;
    this->pinLevelWater = pinLevelWater;
    this->limitWaterRecipient = limitWaterRecipient;
}

void ControllerWDispenser::setup(byte pin)
{
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    this->pin = pin;
}

int ControllerWDispenser::open()
{
    if (this->isOpen())
    {
        return -1;
    }
    else if (this->sonar.isDistanceLimit())
    {
        return -2;
    }
    else if (analogRead(this->pinLevelWater) > this->limitWaterRecipient)
    {
        return -3;
    }

    digitalWrite(this->pin, HIGH);
    return digitalRead(this->pin);
}

int ControllerWDispenser::close()
{
    if (!this->isOpen())
    {
        return -1;
    }

    digitalWrite(this->pin, LOW);
    return digitalRead(this->pin);
}

bool ControllerWDispenser::isOpen()
{
    const int result = digitalRead(this->pin);
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
        Serial.println(command + "ACon:" + String(result));
    }
    else if (analogRead(this->pinLevelWater) > this->limitWaterRecipient && isOpen())
    {
        const int result = close();
        Serial.println(command + "ARes:" + String(result));
    }
}
