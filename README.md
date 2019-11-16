# NYC-MTA-Next-Train

This is a project to create a series of indicator lights to tell you when you need to leave for the next subway train in New York.  It relies on the NYC MTA API and is powered by a raspberry pi and neopixels.  The full writeup can be found:

http://michaelweinberg.org/post/171963532565/pi-powered-mta-subway-alerts

The script expects your API urls to be in a file named config.py in the same directory.  You will need an API key from the MTA in order to access the information.  exampleconfig.py is this repo shows the expected format.

nycmtapi.py is the primary script.

The 'grabber' function is adopted from https://github.com/chris-griffin/real-time 

The files in the /archive folder are ones that I used to figure out how various pieces fit together and are no longer needed.  In part they reflect my original (incorrect) belief that I needed an independent arduino to power the lights.

Hardware License: CERN-OHL-P (draft 9/27/19) or any subsequence CERN-OHL-P
Software License: MIT
Documentation License: CC BY-SA 4.0 Int'l
