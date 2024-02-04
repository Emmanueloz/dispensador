// ControllerDispenser.h
#include <Arduino.h>
#include "Dispensador.h"

class ControllerDispenser
{
private:
    Dispensador &dispensador;
    String command;

public:
    ControllerDispenser(Dispensador &dispensador, String command);
    void processCommand(String command, String value);
    void closeAutomatic();
};
