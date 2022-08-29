"""
Startup script that sets up logging and debugging. Needs to be put in the Blender startup folder on system
"""
import logging

fmt = "%(asctime)-12s %(levelname)-8s %(name)-8s: %(message)s"
dfmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt=dfmt)

def register():
    pass