#include <Arduino.h>
#include "Sonares.h"

#ifndef CONTROLLER_SONAR_H
#define CONTROLLER_SONAR_H

class ControllerSonar
{
private:
    Sonares &sonar;
    String command;

public:
    ControllerSonar(Sonares &sonar, String command);
    void processCommand(String value);
};

#endif // CONTROLLER_SONAR_H