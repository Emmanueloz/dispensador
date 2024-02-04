// ControllerDispenser.h
#include <Arduino.h>
#include "Dispensador.h"
#include "Sonares.h"

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
