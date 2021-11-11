## WLED_E131_PC_client


This is a personal project to control from my computer my RGB led strip+ESP8266+WLED setup. It was not built for the general public, so I will add documentation/update it only if I need or if there are some requests to do it. The program was built on **Windows 10/11** with **Python 3.7** (but I might make it available for linux as well in the future)

##### Basic concepts:

- E131 communication
- full WLED compatible
- RGB effects available:
    + Rainbow
    + Audio Visualizer
    + Screen Mirroring
- Tkinter GUI

---

This code is just a GUI module based on Tkinter that allows you to synchronize your leds with the computer audio, or to mirror the average color of your screen.
These are the effects I was mostly interested in, because WLED already offers a good library of "static" effects (so that don't require a connection to a pc). 
However, this code makes it easier to add any effect to your WLED device, because you can just add a Python function on your pc, instead of having to modify a C++ program and flash the WLED device every time you make a change 

##### E131

It uses the E131 protocol to control a WLED device, so as soon as you start this program it will seamlessly take control of the leds. It should easily be able to control any other framework that supports E131.
The E131 communication is done thanks to the [sacn](https://github.com/Hundemeier/sacn) module, which was slightly modified under its MIT license.

##### Documentation

At the moment, there is no extensive documentation on all the available features or on how to modify the code, but I think it is quite straightforward to understand. Feel free to ask for clarifications.

##### Installation

Right now the code is not properly tested and validated, so binaries are not publicly available.<br>
To install it, make sure to download the dependencies using the `requirements.txt` file, and install PyAudio using the wheel available [at this page](https://www.lfd.uci.edu/~gohlke/pythonlibs/).<br>
To run it, run `main.py` with Python. Again, I have no idea how it behaves on different machines, so be ready to work a bit to fix eventual errors. If you have problems, send a message in the issue section. 
