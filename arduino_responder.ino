#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
int incomingByte; //variable to read incoming serial data
String str;

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

}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the string up until the 'Z' char marks the end
    str = Serial.readStringUntil('Z');

    //york south 

    //first light 
    if (str.indexOf('a') >= 0) {
      //LED number, RGB
      strip.setPixelColor(0, 255, 140, 0);
    }

    //second light 
    if (str.indexOf('b') >= 0) {
      strip.setPixelColor(1, 255, 140, 0);
    } 

    //third light 
    if (str.indexOf('c') >= 0) {
      strip.setPixelColor(2, 255, 140, 0);
    }

    //fourth light 
    if (str.indexOf('d') >= 0) {
      strip.setPixelColor(3, 255, 140, 0);
    }

    //york north 

    //first light 
    if (str.indexOf('3') >= 0) {
      //LED number, RGB
      strip.setPixelColor(4, 255, 140, 0);
    }

    //second light 
    if (str.indexOf('f') >= 0) {
      strip.setPixelColor(5, 255, 140, 0);
    } 

    //third light 
    if (str.indexOf('g') >= 0) {
      strip.setPixelColor(6, 255, 140, 0);
    }

    //fourth light 
    if (str.indexOf('h') >= 0) {
      strip.setPixelColor(7, 255, 140, 0);
    }

    //high south 

    //first light 
    if (str.indexOf('i') >= 0) {
      //LED number, RGB
      strip.setPixelColor(8, 0, 0, 255);
    }

    //second light 
    if (str.indexOf('j') >= 0) {
      strip.setPixelColor(9, 0, 0, 255);
    } 

    //third light 
    if (str.indexOf('k') >= 0) {
      strip.setPixelColor(10, 0, 0, 255);
    }

    //fourth light 
    if (str.indexOf('l') >= 0) {
      strip.setPixelColor(11, 0, 0, 255);
    }

    //high north 

    //first light 
    if (str.indexOf('m') >= 0) {
      //LED number, RGB
      strip.setPixelColor(12, 0, 0, 255);
    }

    //second light 
    if (str.indexOf('n') >= 0) {
      strip.setPixelColor(13, 0, 0, 255);
    } 

    //third light 
    if (str.indexOf('o') >= 0) {
      strip.setPixelColor(14, 0, 0, 255);
    }

    //fourth light 
    if (str.indexOf('p') >= 0) {
      strip.setPixelColor(15, 0, 0, 255);
    }

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
