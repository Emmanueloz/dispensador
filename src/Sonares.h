#include <Arduino.h>
#include <NewPing.h>

class Sonares
{
private:
    NewPing *sonar;
    int limit;

public:
    Sonares(int pinTrigger, int pinEcho, int maxSonar, int limit);
    int getDistance();
    bool isDistanceLimit();
    int getLimit();
};
