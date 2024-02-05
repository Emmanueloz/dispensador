#include <Arduino.h>
#include <Servo.h>
#ifndef DISPENSADOR_H
#define DISPENSADOR_H
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

#endif // DISPENSADOR_H