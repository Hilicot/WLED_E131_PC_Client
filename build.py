from cx_Freeze import setup, Executable
from sys import platform

base = None
if platform == "win32":
    base = "Win32GUI"

executables = [Executable ("main.py",base=base)]

setup ( name = "WLED E131 PC Client",
        #options = options,
        version = "0.1",
        description = "Python client to control a WLED device with the E131 protocol",
        executables = executables )
