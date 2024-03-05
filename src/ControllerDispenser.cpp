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
        Serial.println(dispensador.close());
    }
    else if (value == "1")
    {
        Serial.println(dispensador.open());
    }
    else if (value == "2")
    {
        Serial.println(dispensador.getPosition());
    }
    else
    {
        Serial.println(this->command + ":notFound");
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
