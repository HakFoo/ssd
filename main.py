from machine import Pin, sleep, I2C
import network
import urequests as requests
import time

from ssd1306 import SSD1306_I2C

i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = SSD1306_I2C(128, 64, i2c, addr=0x3c)



net = network.WLAN(network.STA_IF)
net.active(True)


def main():
    if not net.isconnected():
        print('connecting to network...')
        net.connect('NanoDev', 'NanoDev8232')
        while not net.isconnected():
            pass
        print('success')
        print(net.ifconfig())
        try:
            city = requests.get(
                'https://restapi.amap.com/v3/ip?key=e1a2a87d5338cc03afd6d119138d9225')
            # adcode = city['adcode']
            print(city.__dict__)
            
            # req = requests.request('get',
            #            'https://restapi.amap.com/v3/weather/weatherInfo?city{adcode}=&key=e1a2a87d5338cc03afd6d119138d9225')
        except KeyError:
            print('error')
        lcd.text('font8x8', 0, 0, 8)
        lcd.text('font16x16', 0, 20, 16)
        lcd.show()


if __name__ == '__main__':
    main()
