#include <Arduino.h>
#include "Sonares.h"

#ifndef CONTROLLER_W_DISPENSER_H
#define CONTROLLER_W_DISPENSER_H

class ControllerWDispenser
{
private:
    static String command;
    static byte pin;
    static Sonares &sonar;

public:
    static void setup(String command, byte pin, Sonares &sonar);
    static void processCommand(String value);
};

#endif // CONTROLLER_W_DISPENSER_H
