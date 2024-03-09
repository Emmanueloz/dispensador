#include "ControllerWDispenser.h"

void ControllerWDispenser::setup(String command, byte pin, Sonares &sonar)
{
    sonar = sonar;
    command = command;
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
        Serial.println(command + "A:" + String(result));
    }
}
