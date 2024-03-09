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
    byte pinLevelWater;
    int limitWaterRecipient;

public:
    ControllerWDispenser(Sonares &sonar, String command, byte pinLevelWater, int limitWaterRecipient);
    void setup(byte pin);
    int open();
    int close();
    bool isOpen();
    void processCommand(String value);
    void closeAutomatic();
};

#endif // CONTROLLER_W_DISPENSER_H
