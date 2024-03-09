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
    String command;

public:
    ControllerFDispenser(byte pin, int openValue, int closeValue, Sonares &sonar, String command);
    int getPosition();
    int open();
    int close();
    bool isOpen();
    void processCommand(String value);
    void closeAutomatic();
};

#endif // CONTROLLER_F_DISPENSER_H