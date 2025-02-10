#ifndef RuFAConnect_h
#define RuFAConnect_h

#include "Arduino.h"

class RuFAConnect {
  public:
    // Конструктор, инициализация с указанием последовательного порта
    RuFAConnect(HardwareSerial &serial);
    
    // Инициализация библиотеки (например, установка скорости порта)
    void begin(long baudRate);
    
    // Отправка данных на RuFA Connect
    void sendData(const char* data);
    
    // Получение данных от RuFA Connect (если требуется)
    String receiveData();
    
  private:
    HardwareSerial *_serial;  // Указатель на объект последовательного порта
};

#endif
