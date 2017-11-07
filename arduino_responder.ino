#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
int incomingByte; //variable to read incoming serial data
String str;

const int buttonPin = 2; //that's the interrupt button pin
int buttonState = 0;

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(9, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
   // initialize serial communication:
  Serial.begin(9600);

  //for the interrupt
  pinMode(buttonPin, INPUT);

}

void loop() {

  //for checking the interrupt
  buttonState = digitalRead(buttonPin);
  //if the button is pushed 
  if (buttonState == HIGH) {
    //set all of the pixels to off
    for(int x = 0; x < 16; x++) {
       strip.setPixelColor(x, 0, 0, 0);
       }
     //push the changes
     strip.show();
     //wait 4 hours which is 14400000
     delay(90000);
  }
  
  
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the string up until the 'Z' char marks the end
    str = Serial.readStringUntil('Z');

    //york south 

    OrangeLight('a', 0);
    OrangeLight('b', 1);
    OrangeLight('c', 2);
    OrangeLight('d', 3);

    //york north 

    OrangeLight('e', 4);
    OrangeLight('f', 5);
    OrangeLight('g', 6);
    OrangeLight('h', 7);

    //high south 

    BlueLight('i', 8);
    BlueLight('j', 9);
    BlueLight('k', 10);
    BlueLight('l', 11);

    //high north 

    BlueLight('m', 12);
    BlueLight('n', 13);
    BlueLight('o', 14);
    BlueLight('p', 15);

    // off
    if (str.indexOf('Y') >= 0) {
       for(int x = 0; x < 16; x++) {
        strip.setPixelColor(x, 0, 0, 0);
       }
    }
  }

  //pushes the changes to the LEDs
  strip.show();
  
}

void OrangeLight(char letter, int led_number) {
  if (str.indexOf(letter) >= 0) {
    strip.setPixelColor(led_number, 140, 255, 0);
  }
  else {
    strip.setPixelColor(led_number, 0, 0, 0);
  }
}

void BlueLight(char letter, int led_number) {
  if (str.indexOf(letter) >= 0) {
    strip.setPixelColor(led_number, 0, 0, 2);
  }
  else {
    strip.setPixelColor(led_number, 0, 0, 0);
  }
}

