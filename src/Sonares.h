#include <Arduino.h>
#include <NewPing.h>

#ifndef SONARES_H
#define SONARES_H
class Sonares
{
private:
    NewPing *sonar;
    int limit;

public:
    Sonares(byte pinTrigger, byte pinEcho, int maxSonar, int limit);
    int getDistance();
    bool isDistanceLimit();
    int getLimit();
};

#endif // SONARES_H