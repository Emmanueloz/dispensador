#include "ControllerTimeDispenser.h"

ControllerTimeDispenser::ControllerTimeDispenser(String command, long timeOpen, void (*callback)())
    : command(command), timeOpen(timeOpen), callback(callback)
{
    this->ticker = new Ticker(this->callback, this->timeOpen);
}

void ControllerTimeDispenser::start()
{
    this->ticker->start();
}

void ControllerTimeDispenser::update()
{
    this->ticker->update();
}

void ControllerTimeDispenser::processCommand(String command, String value)
{
    if (command == this->command)
    {
        if (value.toInt() > 1000)
        {
            this->timeOpen = value.toInt();
            this->ticker->interval(this->timeOpen);
            Serial.println(this->command + "set:" + this->timeOpen);
        }
        else if (value == "1")
        {
            Serial.println(this->command + "repeat:" + this->ticker->counter());
        }
    }
}
