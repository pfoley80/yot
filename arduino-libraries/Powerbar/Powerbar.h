#ifndef Powerbar_h
#define Powerbar_h

#include "WProgram.h"

class Powerbar {
  public:
    Powerbar(int pin);
    
    boolean state();
    void on();
    void off();
    
    // Returns the state of the powerbar
    boolean toggle();   

    // Toggles the powerbar to the selected state
    void toggle(boolean b);
    
  private:
    int _pin;
};

#endif
    
