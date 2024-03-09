#include <Arduino.h>
#include <Servo.h>
#include "Sonares.h"

#ifndef CONTROLLER_F_DISPENSER_H
#define CONTROLLER_F_DISPENSER_H

class ControllerFDispenser
{
private:
    Servo servo;
    int position;
    int openValue;
    int closeValue;
    Sonares &sonar;
    Sonares &sonarLevel;
    String command;

public:
    ControllerFDispenser(Sonares &sonar, String command, Sonares &sonarLevel);
    void setup(byte pin, int openValue, int closeValue);
    int getPosition();
    int open();
    int close();
    bool isOpen();
    void processCommand(String value);
    void closeAutomatic();
};

#endif // CONTROLLER_F_DISPENSER_H