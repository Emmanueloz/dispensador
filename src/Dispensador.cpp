#include "Dispensador.h"

void Dispensador::setup(byte pin, int openValue, int closeValue)
{
    this->servo.attach(pin);
    this->openValue = openValue;
    this->closeValue = closeValue;
    this->servo.write(this->closeValue);
}

int Dispensador::getPosition()
{

    this->position = this->servo.read();

    return this->position;
}

int Dispensador::open()
{
    const int result = this->getPosition();
    if (result == this->openValue)
    {
        return -1;
    }

    this->servo.write(this->openValue);
    this->position = this->openValue;
    return this->position;
}

int Dispensador::close()
{
    const int result = this->getPosition();
    if (result == this->closeValue)
    {
        return -1;
    }

    this->servo.write(this->closeValue);
    this->position = this->closeValue;
    return this->position;
}

bool Dispensador::isOpen()
{
    this->position = this->getPosition();
    return this->position == this->openValue;
}
