#include <Arduino.h>
#include <Servo.h>
#include "Sonares.h"

#ifndef CONTROLLER_F_DISPENSER_H
#define CONTROLLER_F_DISPENSER_H

class ControllerFDispenser
{
private:
    static Servo servo;
    static int position;
    static int openValue;
    static int closeValue;
    static Sonares &sonar;
    static String command;

public:
    static void setup(byte pin, int openValue, int closeValue, Sonares &sonar, String command);
    static int getPosition();
    static int open();
    static int close();
    static bool isOpen();
    static void processCommand(String value);
    static void closeAutomatic();
};

#endif // CONTROLLER_F_DISPENSER_H