#!/usr/bin/env python
from yeelight import Bulb
import argparse
import re

bulb = Bulb("192.168.1.150")

# CLI help message stuff
parser = argparse.ArgumentParser()
help = "What to set. Can be power, color, temp, bright"
choices = ["power", "color", "temp", "bright"]
parser.add_argument("command", help=help, metavar='command', choices=choices)
parser.add_argument("arg", help='command-specific arg. "on", "red", etc.')
args = parser.parse_args()


def power_on():
    bulb.turn_on()


def power_off():
    bulb.turn_off()


def power_toggle():
    bulb.toggle()


def color_red():
    bulb.set_rgb(255, 0, 0)


def color_green():
    bulb.set_rgb(0, 255, 0)


def color_blue():
    bulb.set_rgb(0, 0, 255)


def color_accent():
    bulb.set_rgb(0, 243, 200)


def color_hex(hex):
    hex = hex.lstrip('#')
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    bulb.set_rgb(red, green, blue)


# The yeelight module gracefully handles out of range values, so we only warn
# the user if the value is out of range
def set_brightness(bright):
    if bright not in range(1, 101):
        print("Value out of range (1-100). Using closest valid value...")
    bulb.set_brightness(bright)


def set_temperature(temp):
    if temp not in range(2500, 6501):
        print("Value out of range (2500-6500). Using closest valid value...")
    bulb.set_color_temp(temp)


if args.command == "power":
    switcher = {
        'on': power_on,
        'off': power_off,
        'toggle': power_toggle,
    }
    func = switcher.get(args.arg, lambda: print('Invalid argument.\
    Supported args: "on", "off", "toggle"'))
    func()

if args.command == "color":
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args.arg):
        hex = args.arg
        args.arg = 'hex'
    switcher = {
        'red': color_red,
        'green': color_green,
        'blue': color_blue,
        'hex': color_hex,
    }
    func = switcher.get(args.arg, lambda: print('Invalid argument.\
    Supported args: "red", "green", "blue", "white", or "#hex"'))
    if args.arg == 'hex':
        func(hex)
    else:
        func()

if args.command == "bright":
    try:
        bright = int(args.arg)
    except ValueError:
        exit("Not a number")
    set_brightness(bright)

if args.command == "temp":
    try:
        temp = int(args.arg)
    except ValueError:
        exit("Not a number")
    set_temperature(temp)
