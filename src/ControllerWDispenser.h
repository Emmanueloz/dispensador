#include <Arduino.h>
#include "Sonares.h"

#ifndef CONTROLLER_W_DISPENSER_H
#define CONTROLLER_W_DISPENSER_H

class ControllerWDispenser
{
private:
    String command;
    byte pin;
    Sonares &sonar;

public:
    ControllerWDispenser(byte pin, Sonares &sonar, String command);
    int open();
    int close();
    bool isOpen();
    void processCommand(String value);
    void closeAutomatic();
};

#endif // CONTROLLER_W_DISPENSER_H
