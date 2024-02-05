#include <Ticker.h>
#include "Dispensador.h"

#ifndef CONTROLLER_TIME_DISPENSER_H
#define CONTROLLER_TIME_DISPENSER_H

class ControllerTimeDispenser
{
private:
    String command;
    Ticker *ticker;
    long timeOpen;
    void (*callback)();

public:
    ControllerTimeDispenser(String command, long timeOpen, void (*callback)());
    void start();
    void update();
    void processCommand(String command, String value);
};

#endif // CONTROLLER_TIME_DISPENSER_H