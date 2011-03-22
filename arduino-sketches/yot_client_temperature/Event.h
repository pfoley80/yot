// Provides YOT event generation and handling.

#ifndef Event_h
#define Event_h
#include "WProgram.h"

#define MAX_EVENT_TYPES 64
#define MAX_HANDLERS 64

class Event {
  public:
  
    // Event structure
    struct event {
      short int type;
      double utc_epoch_time_ms;
      byte data[];
    };  

    typedef void (*event_handler)(event*);
  
    // Core event types
    const static int REGISTER_EVENT_TYPE = 0;
    const static int UNREGISTER_EVENT_TYPE = 1;
    
    Event();
    
    // Register an event type in the system. Returns false if no more event types can be registered
    boolean register_type(int type);
    
    // Unregister an event. Returns false if an event type cannot be found
    boolean unregister_type(int type);
    
    // Bind a single (for now) handler to the event type
    boolean bind_handler(int type, event_handler *handler);
    boolean unbind_handler(int type, event_handler *handler);
    
    // Push an event into the event queue. If the queue is
    // full, returns false
    boolean push_event(event *evt);
    
    // Pop an event from the front of the queue (oldest inserted)
    boolean pop_event(event *evt);
    
    // Handlers for core types
    // TODO
    
  private:
    static int _event_types[MAX_EVENT_TYPES];
    static int _event_types_count;
    
    static int _handlers[MAX_HANDLERS];
    static int _handlers_count;
};

#endif
