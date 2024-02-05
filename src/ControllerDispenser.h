#include <Arduino.h>
#include "Dispensador.h"
#include "Sonares.h"

#ifndef CONTROLLER_DISPENSER_H
#define CONTROLLER_DISPENSER_H
class ControllerDispenser
{
private:
    Dispensador &dispensador;
    Sonares &sonar;
    String command;

public:
    ControllerDispenser(Dispensador &dispensador, Sonares &sonar, String command);
    void processCommand(String command, String value);
    void closeAutomatic();
};

#endif // CONTROLLER_DISPENSER_H