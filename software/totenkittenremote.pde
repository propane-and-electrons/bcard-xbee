#include <Button.h>
#include <XBee.h>

XBee xbee = XBee();

XBeeAddress64 remoteAddress = XBeeAddress64(0x0013a200, 0x4064F906);
uint8_t on[] = {5};
uint8_t off[] = {4};
uint8_t D0[] = {'D','0'};
RemoteAtCommandRequest reqon  = RemoteAtCommandRequest(remoteAddress, D0, on, 1);
RemoteAtCommandRequest reqoff = RemoteAtCommandRequest(remoteAddress, D0, off, 1);
RemoteAtCommandResponse response;

const int ledPin = 13;
Button button = Button(2, PULLUP);

void setup() {
  pinMode(ledPin, OUTPUT); 
  xbee.begin(57600);
  delay(5000);
}

void loop() {

  if(button.uniquePress()) {
    digitalWrite(ledPin, HIGH);
    xbee.send(reqon);
  }
  else if(button.stateChanged()) {
    digitalWrite(ledPin, LOW);
    xbee.send(reqoff);
  } 
  
}
