#ifndef RuFAConnect_h
#define RuFAConnect_h

#include "Arduino.h"

class RuFAConnect {
  public:
    RuFAConnect(HardwareSerial &serial);
    
    void begin(long baudRate);
    
    void sendData(const char* data);
    
    String receiveData();
    
  private:
    HardwareSerial *_serial; 
};

#endif
