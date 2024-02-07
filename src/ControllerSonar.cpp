#include "ControllerSonar.h"

ControllerSonar::ControllerSonar(Sonares &sonar, String command) : sonar(sonar), command(command) {}

void ControllerSonar::processCommand(String value)
{
    if (value == "1")
    {
        Serial.println(this->command + "get:" + sonar.getDistance());
    }
    else if (value == "2")
    {
        String result = sonar.isDistanceLimit() ? "true" : "false";
        Serial.println(this->command + "Is:" + result);
    }
    else
    {
        Serial.println(this->command + ":notFound");
    }
}
