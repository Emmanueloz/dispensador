#include "ControllerTimeDispenser.h"

char ControllerTimeDispenser::getTypeTime(String time)
{
    time.toLowerCase();

    if (time.indexOf("s") != -1)
    {
        return 's';
    }
    else if (time.indexOf("m") != -1)
    {
        return 'm';
    }
    else if (time.indexOf("h") != -1)
    {
        return 'h';
    }
    return 'N';
}

long ControllerTimeDispenser::convertTimeToMillis(String time, char type)
{
    String value = time.substring(0, type);
    if (type == 's')
    {
        return value.toInt() * this->SECONDS;
    }
    else if (type == 'm')
    {
        return value.toInt() * this->MINUTES;
    }
    else if (type == 'h')
    {
        return value.toInt() * this->HOURS;
    }
    else
    {
        return -1;
    }
}

long ControllerTimeDispenser::convertMillisToTime()
{
    if (this->typeTime == 's')
    {
        return this->timeOpen / this->SECONDS;
    }
    else if (this->typeTime == 'm')
    {
        return this->timeOpen / this->MINUTES;
    }
    else if (this->typeTime == 'h')
    {
        return this->timeOpen / this->HOURS;
    }
    else
    {
        return -1;
    }
}

ControllerTimeDispenser::ControllerTimeDispenser(String command, unsigned long timeOpen, char typeTime, void (*callback)())
    : command(command), timeOpen(timeOpen), callback(callback)
{
    this->ticker = new Ticker(this->callback, this->timeOpen);
    this->typeTime = typeTime;
}

String ControllerTimeDispenser::getTimer()
{

    return String(this->convertMillisToTime()) + this->typeTime;
}

void ControllerTimeDispenser::start()
{
    this->ticker->start();
}

void ControllerTimeDispenser::update()
{
    this->ticker->update();
}

void ControllerTimeDispenser::processCommand(String value)
{
    if (this->getTypeTime(value) != 'N')
    {
        this->typeTime = this->getTypeTime(value);
        this->timeOpen = this->convertTimeToMillis(value, this->typeTime);
        this->ticker->interval(this->timeOpen);
        Serial.println(this->command + "set:" + value);
    }
    else if (value == "1")
    {
        Serial.println(this->command + "repeat:" + this->ticker->counter());
    }
    else if (value == "2")
    {
        Serial.println(this->command + "get:" + this->getTimer());
    }
    else
    {
        Serial.println(this->command + ":notFound");
    }
}
