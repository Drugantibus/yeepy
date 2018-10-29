#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
from yeelight import *
import argparse, argcomplete
import re

bulb = Bulb("192.168.1.150")

parser = argparse.ArgumentParser()
parser.add_argument("command", help="What to set. Can be power, color, temp, bright", metavar='command', choices = ["power", "color", "temp", "bright"])
parser.add_argument("arg", help='command-specific arg. "on", "red", etc.')
argcomplete.autocomplete(parser)
args = parser.parse_args()

def color_red():
    bulb.set_rgb(255, 0, 0)

def color_green():
    bulb.set_rgb(0, 255, 0)

def color_blue():
    bulb.set_rgb(0, 0, 255)

def color_hex(hex):
    hex = hex.lstrip('#')
    tup = tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))
    red, green, blue = tup
    bulb.set_rgb(red, green, blue)

if args.command == "power":
    valid = ['on','off','toggle']
    if args.arg in valid:
        if args.arg == 'on':
            bulb.turn_on()
        if args.arg == 'off':
            bulb.turn_off()
        if args.arg == 'toggle':
            bulb.toggle()
    else:
        print('Invalid argument. Supported args: "on", "off", "toggle"')

if args.command == "color":
    valid = ['red', 'green', 'blue', 'white']
    is_hex =
    if args.arg in valid or re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args.arg):
        if args.arg == 'red':
            bulb.set_rgb(255, 0, 0)

        if args.arg == 'green':
            bulb.set_rgb(0, 255, 0)
            break
        if args.arg == 'blue':
            bulb.set_rgb(0, 0, 255)
            break
        if args.arg == 'white':
            bulb.set_rgb(255, 255, 255)
            break
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args.arg):
            args.arg = args.arg.lstrip('#')
            tup = tuple(int(args.arg[i:i+2], 16) for i in (0, 2 ,4))
            red, green, blue = tup
            bulb.set_rgb(red, green, blue)
            break
    else:
        print('Invalid argument. Supported args: "red", "green", "blue", "white", or "#hex"')
if args.command == "bright":
    try:
        bright = int(args.arg)
    except:
        exit("Not a number")
    if bright in range(1,101):
        bulb.set_brightness(bright)
    else:
        print("Out of range. Use a number 1-100")
if args.command == "temp":
    try:
        temp = int(args.arg)
    except:
        exit("Not a number")
    if temp >= 2500 and temp <= 6500:
        bulb.set_color_temp(temp)
    else:
        print("Out of range. Use a number 2500-6500")
