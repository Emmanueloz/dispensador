#include <Ticker.h>
#include "Dispensador.h"

#ifndef CONTROLLER_TIME_DISPENSER_H
#define CONTROLLER_TIME_DISPENSER_H

class ControllerTimeDispenser
{
private:
    String command;
    Ticker *ticker;
    unsigned long timeOpen;
    char typeTime;
    void (*callback)();
    const long SECONDS = 1000;
    const long MINUTES = 60000;
    const long HOURS = 3600000;
    char getTypeTime(String time);
    long convertTimeToMillis(String time, char type);
    long convertMillisToTime();

public:
    ControllerTimeDispenser(String command, unsigned long timeOpen, char typeTime, void (*callback)());
    void start();
    void update();
    void processCommand(String command, String value);
};

#endif // CONTROLLER_TIME_DISPENSER_H
