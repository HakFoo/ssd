from machine import Pin, I2C
import network
import urequests as requests
import ujson as json
import time
from ssd1306 import SSD1306_I2C
from HZK import HZK

i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 高德地图 token
token = 'e1a2a87d5338cc03afd6d119138d9225'


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


def show_zh(zh_str, x_axis, y_axis):
    global oled
    words = 0
    for k in zh_str:
        byte_data = HZK(k)
        data_len = len(byte_data)
        zh_size = 0

    for i in range(8, 65):
        num = int((i-1)/8)+1
        if((data_len/num) == i):
            ch_size = i
            break

    if ch_size == 0:
        print(k, "字模，数据量不匹配，无法显示。")
    else:
        for i in range(0, num):
            for y in range(ch_size*i, ch_size*(i+1)):
                a = '{:0>8b}'.format(byte_data[y])
                for x in range(0, 8):
                    oled.pixel(x_axis + words + x+8*i, y %
                               ch_size + y_axis, int(a[x]))

        words += ch_size


def main():
    linked_network()
    try:
        # 高德地图天气API
        city, adcode = get_city(token)
        get_lives_weather(adcode, token)
    except KeyError:
        print('error')

    show_zh('你好', 0, 0)
    # oled.text('font16x16', 0, 20, 16)
    oled.show()


if __name__ == '__main__':
    main()
