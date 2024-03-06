// ControllerDispenser.cpp
#include "ControllerDispenser.h"

ControllerDispenser::ControllerDispenser(Dispensador &dispensador, Sonares &sonar, String command) : dispensador(dispensador), sonar(sonar)
{
    this->command = command;
}

void ControllerDispenser::processCommand(String value)
{
    if (value == "0")
    {
        int result = dispensador.close();
        Serial.println(this->command + "R:" + String(result));
    }
    else if (value == "1")
    {
        int result = dispensador.open();
        Serial.println(this->command + "R:" + String(result));
    }
    else if (value == "2")
    {
        int result = dispensador.getPosition();
        Serial.println(this->command + "P:" + String(result));
    }
    else
    {
        Serial.println(this->command + ":notFound")
    }
}

void ControllerDispenser::closeAutomatic()
{

    if (sonar.isDistanceLimit() && dispensador.isOpen())
    {
        Serial.println(this->command + "A:0");
        this->dispensador.close();
    }
}
