#ifndef EventParser_h
#define EventParser_h
#include "WProgram.h"
#include "Event.h"

class EventParser {
  public:
    typedef void (*eventhandler)(Event *event);

    EventParser();
    ~EventParser();
    EventParser& concat(char c);
    
    boolean register_handler(char *type, eventhandler handler, int *type_int);
    eventhandler lookup_handler(char *type);
    
    void eos();    
    void reset();
    
  private:
    static const char TOKEN_START = 't';
    static const char TOKEN_SEP = '\n';
    static const char TOKEN_TOTAL_SEP = ':';
    static const char TOKEN_EVENT_SEP = ':';

    static const int STATE_WAITING = 0;
    static const int STATE_START = 1;
    static const int STATE_TOTAL = 2;
    static const int STATE_EVENT_TYPE = 3;
    static const int STATE_EVENT_DATA = 4;
    static const int STATE_END = 5;
    static const int STATE_EOS = 6;
    
    int MAX_BUFFER;    

    char *char_buffer;
    int char_buffer_offset;  
    int state;
    
    int total;
    int count;

    Event temp_event;

    // TODO: This should be dynamic, but it'll do for now    
    static const int MAX_HANDLERS = 16;

    eventhandler handlers[MAX_HANDLERS];
    char *handlers_type_map[MAX_HANDLERS];
    int handlers_last_index;
  
    void clear_buffer();
    boolean push_buffer(char c);    
};
  
#endif 
