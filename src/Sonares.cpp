#include "Sonares.h"

Sonares::Sonares(int pinTrigger, int pinEcho, int maxSonar, int limit)
{
    this->sonar = new NewPing(pinTrigger, pinEcho, maxSonar);
    this->limit = limit;
}

int Sonares::getDistance()
{
    return this->sonar->ping_cm();
}

bool Sonares::isDistanceLimit()
{
    return this->getDistance() >= this->limit;
}

int Sonares::getLimit()
{
    return this->limit;
}
