// ControllerDispenser.cpp
#include "ControllerDispenser.h"

ControllerDispenser::ControllerDispenser(Dispensador &dispensador, Sonares &sonar, String command) : dispensador(dispensador), sonar(sonar), command(command)
{
}

void ControllerDispenser::processCommand(String command, String value)
{

    if (command == this->command)
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
    }
}

void ControllerDispenser::closeAutomatic()
{

    if (sonar.isDistanceLimit() && dispensador.isOpen())
    {
        Serial.println(this->command + "Count:0");
        this->dispensador.close();
    }
}
