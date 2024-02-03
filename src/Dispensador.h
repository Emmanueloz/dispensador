#include <Arduino.h>
#include <Servo.h>

class Dispensador
{
private:
    Servo servo;
    int position;
    int openValue;
    int closeValue;

public:
    void setup(byte pin, int openValue, int closeValue);
    int getPosition();
    int open();
    int close();
    bool isOpen();
};
