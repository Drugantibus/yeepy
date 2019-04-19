from yeelight import Bulb

class WhiteBulb:
    def __init__(self, ip):
        self.bulb = Bulb(ip)

    def power_on(self):
        self.bulb.turn_on()
        print("Turning the light on...")


    def power_off(self):
        self.bulb.turn_off()
        print("Turning the light off...")


    def power_toggle(self):
        self.bulb.toggle()
        print("Toggling the light...")    

    def set_brightness(self,bright):
        self.bulb.set_brightness(bright)
        print("Setting the brightness to ", bright, "%...")


    def set_temperature(self,temp):
        self.bulb.set_color_temp(temp)
        print("Setting the temperature to ", temp, "K...")


    def get_status(self):
        status = self.bulb.get_properties()
        power = status['power']
        bright = status['bright']
        temp = status['ct']
        rgb = status['rgb']
        r, g, b = [rgb[i:i+3] for i in range(0, len(rgb), 3)]
        rgb = "(" + r + ", " + g + ", " + b + ")"
        print("Power: {}\nBrighness: {}%\nTemperature: {}K\nRGB: {}"
            .format(power, bright, temp, rgb))

class ColorBulb(WhiteBulb):
    def __init__(self, ip):
        super()
        self.bulb = Bulb(ip)
    

    def color_red(self):
        self.bulb.set_rgb(255, 0, 0)
        print("Setting the light to red...")


    def color_green(self):
        self.bulb.set_rgb(0, 255, 0)
        print("Setting the light to green...")


    def color_blue(self):
        self.bulb.set_rgb(0, 0, 255)
        print("Setting the light to blue...")


    def color_white(self):
        self.bulb.set_color_temp(4000)
        print("Setting the light to white...")


    def color_hex(self, hex):
        hex = hex.lstrip('#')
        red, green, blue = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        self.bulb.set_rgb(red, green, blue)
        print("Setting the light to RGB(", str(red), str(green), str(blue),")...")