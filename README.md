# NYC-MTA-Next-Train
Physical display tied to arrival times for NYC subway trains at specific stations


The script expects your API urls to be in a file named config.py in the same directory.  You will need an API key from the MTA in order to access the information.  exampleconfig.py is this repo shows the expected format.

nycmtapi.py is the primary script.

nycmta.py was the script in connection with the arduino.  It is no longer used.

arduino_responder.ino is no longer used. It was written when I was using the arduino to drive the neopixels. Now I am just using the pi GPIO pins.

Importdata.py is not necessary for the final product. I was using it to rebuild the "grabber" function.
