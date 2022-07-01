from machine import Pin, I2C
import network
import lib.urequests as requests
import ujson as json
import time
from lib.ssd1306 import SSD1306_I2C
from lib.ChineseFont import ChineseFont as CF

i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 高德地图 token
token = 'e1a2a87d5338cc03afd6d119138d9225'

c8 = CF('font_8.data')


def linked_network():
    net = network.WLAN(network.STA_IF)
    net.active(True)
    if not net.isconnected():
        net.connect('418', 'funlive6')
        while not net.isconnected():
            pass
        print('network success')
        ip = net.ifconfig()[0]
        print('IP: '+ip)


# 获取adcode与city
def get_city(token):
    try:
        city = requests.get('https://restapi.amap.com/v3/ip?key=' + token)
        adcode = city.json()['adcode']
        city = city.json()['city']
        print('Retrieved adcode: ' + adcode)
        print('Retrieved city: ' + city)
        return city, adcode
    except KeyError:
        print('GET city error')

# 通过adcode获取当前天气


def get_lives_weather(adcode, token):
    try:
        req = requests.get(
            'https://restapi.amap.com/v3/weather/weatherInfo?city='+adcode+'&key='+token)
        print(req.json()['lives'][0])

    except KeyError:
        print('GET weather error')


def main():
    linked_network()
    try:
        # 高德地图天气API
        city, adcode = get_city(token)
        get_lives_weather(adcode, token)
    except KeyError:
        print('error')

    f1 = c8.get_bit_map('好')

    oled.blit(f1, 0, 0)
    # oled.text('font16x16', 0, 20, 16)
    oled.show()


if __name__ == '__main__':
    main()
