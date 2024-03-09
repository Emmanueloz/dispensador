#include "ControllerFDispenser.h"

ControllerFDispenser::ControllerFDispenser(Sonares &sonar, String command, Sonares &sonarLevel) : sonar(sonar), sonarLevel(sonarLevel)
{
    this->command = command;
}

void ControllerFDispenser::setup(byte pin, int openValue, int closeValue)
{
    this->servo.attach(pin);
    this->openValue = openValue;
    this->closeValue = closeValue;
    this->servo.write(closeValue);
}

int ControllerFDispenser::getPosition()
{
    this->position = servo.read();
    return position;
}

int ControllerFDispenser::open()
{
    if (isOpen())
    {
        return -1;
    }
    else if (this->sonar.isDistanceLimit())
    {
        Serial.println(this->sonar.isDistanceLimit());
        return -2;
    }
    else if (!this->sonarLevel.isDistanceLimit())
    {
        return -3;
    }

    this->servo.write(this->openValue);
    this->position = this->openValue;
    return this->position;
}

int ControllerFDispenser::close()
{
    if (!this->isOpen())
    {
        return -1;
    }

    servo.write(closeValue);
    position = closeValue;
    return position;
}

bool ControllerFDispenser::isOpen()
{
    this->position = getPosition();
    // Serial.println("Position: " + String(this->position) + " OpenValue: " + String(this->openValue));
    return this->position == this->openValue;
}

void ControllerFDispenser::processCommand(String value)
{
    if (value == "0")
    {
        int result = close();
        result = 0 ? result == this->closeValue : result;
        Serial.println(this->command + "R:" + String(result));
    }
    else if (value == "1")
    {
        int result = open();
        result = 1 ? result == this->openValue : result;
        Serial.println(this->command + "R:" + String(result));
    }
    else if (value == "2")
    {
        int result = getPosition();
        result = 1 ? result == this->openValue : 0;
        Serial.println(this->command + "P:" + String(result));
    }
    else
    {
        Serial.println(this->command + ":notFound");
    }
}

void ControllerFDispenser::closeAutomatic()
{
    if (sonar.isDistanceLimit() && isOpen())
    {
        const int result = close();
        Serial.println(this->command + "ACon:" + String(result));
    }
    else if (!sonarLevel.isDistanceLimit() && isOpen())
    {
        const int result = close();
        Serial.println(this->command + "ARes:" + String(result));
    }
}
