#include "WProgram.h"
#include "Temperature.h"

Temperature::Temperature(int pin) {
  _pin = pin;
  _sample_size = SAMPLE_SIZE;
  _sample_count = 0;
  _avg = 0;
  _averaged = false;  
}

int Temperature::set_sample_size(int sample_size) {
  int old = _sample_size;
  _sample_size = sample_size;
  return old;
}

int Temperature::get_sample_size() {
  return _sample_size;
}

boolean Temperature::set_averaged(boolean averaged) {
  boolean old = _averaged;
  _averaged = averaged;
  return old;
}

boolean Temperature::get_averaged() {
  return _averaged;
}

boolean Temperature::get_temperature(double *temp) {  
  // This gives a precision of 1/1024
  int analog = analogRead(_pin);
  *temp = ARDUINO_VOLTAGE * 100 * ((double) analog / 1024.0) - 50;
  _avg += *temp;
  
  if (!_averaged)
    return true;
  
  if (_sample_count == _sample_size) {
    *temp = _avg / (double) _sample_size;
    _avg = 0;
    _sample_count = 0;
    return true;
  }
  else {
    _sample_count += 1;
    return false;
  }
}
