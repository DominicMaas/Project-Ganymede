# See https://github.com/DominicMaas/AstroHelper

# Project-Ganymede
A react client + node server that runs on a raspberry bi, allowing remote control of DLSR cameras from a mobile phone.

## Problem

Previously I used a program on my Surface connected to my camera to take astrophotography shots. But this was not ideal for a few reasons. 
Bulky device to carry around, needing a place to put it, large screen ruined night vision etc. I have now also switched to a MacBook, which does not have this software.

## Solution

This repo contains a two part system. 

A python script is run on a raspberry pi (on startup) which looks for a connected camera, and exposes an HTTP API to interact with the camera.

A client-size react app interacts with this API, allowing the ability to set different camera settings, take preview photos, and schedule many photos to be taken at once.

## Future Improvements

- Currently this system relys on both devices being conneceted to the same WiFi network. This may work well for my back garden, but not other locations. I'd like to move to 
bluetooth (I've taken a look, seems painful), Wi-Fi direct or something else.
- Switch the app to flutter (currently the app runs within the browser and a pusdo PWA (at least on iOS).
