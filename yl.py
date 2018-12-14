#!/usr/bin/env python
from yeelight import Bulb
import configparser
import argparse
import re
import socket
import os

# Used to have a correct feedback output when using out of range values for bright and temp
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def power_on():
    bulb.turn_on()
    print("Turning the light on...")


def power_off():
    bulb.turn_off()
    print("Turning the light off...")


def power_toggle():
    bulb.toggle()
    print("Toggling the light...")


def color_red():
    bulb.set_rgb(255, 0, 0)
    print("Setting the light to red...")


def color_green():
    bulb.set_rgb(0, 255, 0)
    print("Setting the light to green...")


def color_blue():
    bulb.set_rgb(0, 0, 255)
    print("Setting the light to blue...")


def color_white():
    bulb.set_color_temp(4000)
    print("Setting the light to white...")


def color_hex(hex):
    hex = hex.lstrip('#')
    red, green, blue = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    bulb.set_rgb(red, green, blue)
    print("Setting the light to RGB(", str(red), str(green), str(blue),")...")

# TODO: Choose between "graceful" out of range handling (this) or hard (argparse choices)
# (it's both ATM)
def set_brightness(bright):
    if bright not in range(1, 101):
        print("Value out of range (1-100). Using closest valid value...")
        bright = clamp(bright, 1, 100)
    bulb.set_brightness(bright)
    print("Setting the brightness to ", bright, "%...")


def set_temperature(temp):
    if temp not in range(2500, 6501):
        print("Value out of range (2500-6500). Using closest valid value...")
    bulb.set_color_temp(temp)
    print("Setting the temperature to ", temp, "K...")


def get_status():
    status = bulb.get_properties()
    power = status['power']
    bright = status['bright']
    temp = status['ct']
    rgb = status['rgb']
    r, g, b = [rgb[i:i+3] for i in range(0, len(rgb), 3)]
    rgb = "(" + r + ", " + g + ", " + b + ")"
    print("Power: {}\nBrighness: {}%\nTemperature: {}K\nRGB: {}"
          .format(power, bright, temp, rgb))


def config_bulb_ip():
    bulb_ip = input("Please enter your bulb's IP address: ")
    try:
        socket.inet_aton(bulb_ip)
        config['DEFAULT']['BULB_IP'] = bulb_ip
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except socket.error:
        print("Invalid IP address. Please try again.")
        config_bulb_ip()


config = configparser.ConfigParser()
config.read('config.ini')

try:
    bulb = Bulb(config['DEFAULT']['BULB_IP'])
except KeyError as e:
    print("You have not configured your bulb yet.")
    config_bulb_ip()
    bulb = Bulb(config['DEFAULT']['BULB_IP'])

# CLI help message stuff
# TODO: show help message when called with no arguments
parser = argparse.ArgumentParser()
parser.add_argument('--reset', action='store_true',
                    help="Delete the stored bulb's IP")

subparsers = parser.add_subparsers(help='command')

parser_power = subparsers.add_parser("power", help='Turn the bulb on or off')
parser_power.add_argument('power_value', choices=['on', 'off', 'toggle'],
                          help='Supported commands')

parser_bright = subparsers.add_parser("bright", help="Set the bulb's brightness")
parser_bright.add_argument('bright_value', type=int, choices=range(1,101),
                           help='Brightness value, 1-100', metavar="value")

parser_color = subparsers.add_parser("color", help="Set the bulb's color")
parser_color.add_argument('color_value',
                          help='Supported colors: red, green, blue, white, or "#HEX"',
                          metavar="value")

parser_temp = subparsers.add_parser("temp", help="Set the bulb's white temperature")
parser_temp.add_argument('temp_value', choices=range(2500,6501), type=int,
                         help="Temperature value, 2500-6500", metavar="value" )

parser_status = subparsers.add_parser("status", help="Get the bulb's current status")
parser_status.add_argument("status", action="store_true",
                           help="Get the bulb's current status")

args = parser.parse_args()


if hasattr(args, 'power_value'):
    switcher = {
        'on': power_on,
        'off': power_off,
        'toggle': power_toggle
    }
    func = switcher.get(args.power_value)
    func()

if hasattr(args, 'bright_value'):
    set_brightness(args.bright_value)

if hasattr(args, 'temp_value'):
    set_temperature(args.temp_value)

if hasattr(args, 'color_value'):
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args.color_value):
        hex = args.color_value
        args.color_value = 'hex'
    switcher = {
        'red': color_red,
        'green': color_green,
        'blue': color_blue,
        'white': color_white,
        'hex': color_hex,
    }
    func = switcher.get(args.color_value, lambda: print('Invalid argument.\
    Supported args: red, green, blue, white, or "#hex"'))
    if args.color_value == 'hex':
        func(hex)
    else:
        func()

if hasattr(args, 'status'):
    get_status()

if args.reset is True:
    os.remove('config.ini')
