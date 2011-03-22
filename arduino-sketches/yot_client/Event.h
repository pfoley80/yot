// Provides YOT event generation and handling.

#ifndef Event_h
#define Event_h
#include "WProgram.h"

class Event {
  public:
    char *type;
    char* data;
  
    Event();
    Event(char *type);
    ~Event();
    
    void set_type(char *data);    
    void set_data(char *data); 
};

#endif
