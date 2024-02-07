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
    byte pinButton;

public:
    ControllerDispenser(Dispensador &dispensador, Sonares &sonar, String command, byte pinButton);
    void processCommand(String value);
    void closeAutomatic();
    void listenButton();
};

#endif // CONTROLLER_DISPENSER_H