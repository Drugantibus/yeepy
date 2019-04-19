#!/usr/bin/env python
from yeelight import Bulb
import configparser
import argparse
import re
import socket
import os
from YeeBulb import ColorBulb, WhiteBulb


# Used to have a correct feedback output when using out of range values for bright and temp
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def config_bulb_ip():
    bulb_ip = input("Please enter your bulb's IP address: ")
    bulb_type = input("Is this an RGB lightbulb? (y/n): ")
    bulb_type = 'color' if bulb_type == ('y' or 'yes') else 'white'
    try:
        socket.inet_aton(bulb_ip)
        config['DEFAULT']['BULB_IP'] = bulb_ip
        config['DEFAULT']['BULB_TYPE'] = bulb_type
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except socket.error:
        print("Invalid IP address. Please try again.")
        config_bulb_ip()


config = configparser.ConfigParser()
config.read('config.ini')

# CLI help message stuff
# TODO: show help message when called with no arguments
parser = argparse.ArgumentParser(epilog="You can also use the initial of each command.")
parser.add_argument('--reset', action='store_true',
                    help="Delete the stored bulb's IP")

subparsers = parser.add_subparsers(help='command')

# Power
parser_power = subparsers.add_parser("power", help='Turn the bulb on or off')
parser_power.add_argument('power_value', choices=['on', 'off', 'toggle'], help='Supported commands')
parser_power = subparsers.add_parser("p")
parser_power.add_argument('power_value', choices=['on', 'off', 'toggle'], help='Supported commands')

# Brightness
parser_bright = subparsers.add_parser("bright" or "b", help="Set the bulb's brightness")
parser_bright.add_argument('bright_value', type=int, help='Brightness value, 1-100', metavar="value")
parser_bright = subparsers.add_parser("b")
parser_bright.add_argument('bright_value', type=int, help='Brightness value, 1-100', metavar="value")

# Color
parser_color = subparsers.add_parser("color", help="Set the bulb's color")
parser_color.add_argument('color_value', help='Supported colors: red, green, blue, white, or "#HEX"', metavar="value")
parser_color = subparsers.add_parser("c")
parser_color.add_argument('color_value', metavar="value")

# Temperature
parser_temp = subparsers.add_parser("temp", help="Set the bulb's white temperature")
parser_temp.add_argument('temp_value', type=int, help="Temperature value, 2500-6500", metavar="value" )
parser_temp = subparsers.add_parser("t")
parser_temp.add_argument('temp_value', type=int, help="Temperature value, 2500-6500", metavar="value" )

# Status
parser_status = subparsers.add_parser("status", help="Get the bulb's current status")
parser_status.add_argument("status", action="store_true", help="Get the bulb's current status")
parser_status = subparsers.add_parser("s")
parser_status.add_argument("status", action="store_true", help="Get the bulb's current status")

args = parser.parse_args()

try:
    if config['DEFAULT']['BULB_TYPE'] == 'color':
        bulb = ColorBulb(config['DEFAULT']['BULB_IP'])
    else:
        bulb = WhiteBulb(config['DEFAULT']['BULB_IP'])
except KeyError as e:
    print("You have not configured your bulb yet.")
    config_bulb_ip()
    if config['DEFAULT']['BULB_TYPE'] == 'color':
        bulb = ColorBulb(config['DEFAULT']['BULB_IP'])
    else:
        bulb = WhiteBulb(config['DEFAULT']['BULB_IP'])


if hasattr(args, 'power_value'):
    switcher = {
        'on': bulb.power_on,
        'off': bulb.power_off,
        'toggle': bulb.power_toggle
    }
    func = switcher.get(args.power_value)
    func()

if hasattr(args, 'bright_value'):
    bright = args.bright_value
    if bright not in range(1, 101):
            print("Value out of range (1-100). Using closest valid value...")
            bright = clamp(bright, 1, 100)
    bulb.set_brightness(bright)

if hasattr(args, 'temp_value'):
    temp = args.temp_value
    if temp not in range(2500, 6501):
            print("Value out of range (2500-6500). Using closest valid value...")
            temp = clamp(temp, 2500, 6500)
    bulb.set_temperature(temp)

if hasattr(args, 'color_value'):
    if isinstance(bulb, WhiteBulb):
        print("This function isn't supported by non-RGB lightbulbs.")
        exit()
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args.color_value):
        hex = args.color_value
        args.color_value = 'hex'
    switcher = {
        'red' or 'r': bulb.color_red,
        'green' or 'g': bulb.color_green,
        'blue' or 'b': bulb.color_blue,
        'white' or 'w': bulb.color_white,
        'hex': bulb.color_hex,
    }
    func = switcher.get(args.color_value, lambda: print('Invalid argument.\
    Supported args: red, green, blue, white, or "#hex"'))
    if args.color_value == 'hex':
        func(hex)
    else:
        func()

if hasattr(args, 'status'):
    bulb.get_status()

if args.reset is True:
    os.remove('config.ini')
