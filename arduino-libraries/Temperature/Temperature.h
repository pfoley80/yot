#ifndef Temperature_h
#define Temperature_h

#include "WProgram.h"
#define ARDUINO_VOLTAGE 5.0
#define SAMPLE_SIZE 10

class Temperature {
  public:
    Temperature(int pin);
    
    int set_sample_size(int sample_size);
    int get_sample_size();
    
    // Requests that that temperature be averaged. Returns whether the temperature was being averaged
    boolean set_averaged(boolean average);
    
    // Returns whether the temperature was being averaged
    boolean get_averaged();
    
    // Gets the temperature.
    // Returns false if the temperature is being averaged and not a final measurement.
    // Returns true if the temperature is not being averaged or if it is being averaged and is a final measurement
    boolean get_temperature(double *temperature);
    
  private:
    int _pin;
    int _sample_size;
    int _sample_count;
    int _avg;
    boolean _averaged;
};

#endif
