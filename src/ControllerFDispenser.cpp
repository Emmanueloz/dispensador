#include "ControllerFDispenser.h"

ControllerFDispenser::ControllerFDispenser(byte pin, int openValue, int closeValue, Sonares &sonar, String command, Sonares &sonarLevel) : sonar(sonar), sonarLevel(sonarLevel)
{
    servo.attach(pin);
    openValue = openValue;
    closeValue = closeValue;
    servo.write(closeValue);
    command = command;
}

int ControllerFDispenser::getPosition()
{
    position = servo.read();

    return position;
}

int ControllerFDispenser::open()
{
    if (isOpen())
    {
        return -1;
    }
    else if (sonar.isDistanceLimit())
    {
        return -2;
    }
    else if (!sonarLevel.isDistanceLimit())
    {
        return -3;
    }

    servo.write(openValue);
    position = openValue;
    return position;
}

int ControllerFDispenser::close()
{
    if (!isOpen())
    {
        return -1;
    }

    servo.write(closeValue);
    position = closeValue;
    return position;
}

bool ControllerFDispenser::isOpen()
{
    position = getPosition();
    return position == openValue;
}

void ControllerFDispenser::processCommand(String value)
{
    if (value == "0")
    {
        const int result = close();
        Serial.println(command + "R:" + String(result));
    }
    else if (value == "1")
    {
        int result = open();
        Serial.println(command + "R:" + String(result));
    }
    else if (value == "2")
    {
        int result = getPosition();
        Serial.println(command + "P:" + String(result));
    }
    else
    {
        Serial.println(command + ":notFound");
    }
}

void ControllerFDispenser::closeAutomatic()
{
    if (sonar.isDistanceLimit() && isOpen())
    {
        const int result = close();
        Serial.println(command + "A:Con" + String(result));
    }
    else if (!sonarLevel.isDistanceLimit() && isOpen())
    {
        const int result = close();
        Serial.println(command + "A:Res" + String(result));
    }
}
