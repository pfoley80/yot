#include "WProgram.h"
#include "Powerbar.h"

Powerbar::Powerbar(int pin) {
  _pin = pin;
}

boolean Powerbar::state() {
  pinMode(_pin, INPUT);
  return digitalRead(_pin);
}

void Powerbar::on() {
  pinMode(_pin, OUTPUT);
  digitalWrite(_pin, HIGH);
}
  
void Powerbar::off() {
  pinMode(_pin, OUTPUT);
  digitalWrite(_pin, LOW);
}
 
void Powerbar::toggle(boolean b) {
   if (b)
      on();
   else
      off();
}

boolean Powerbar::toggle() {
  boolean s = state();
  if (s)
    off();
  else
    on();
    
  return !s;
}

