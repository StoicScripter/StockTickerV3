# general imports
import os.path
import socket
import logging
import qrcode
import math
import time

# import PIL
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
# plotting
# TODO import raspberry pi components
# import waveshare components
from waveshare_epd import epd7in5bc

import json
# formatting
import locale
# util
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

# paths
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
#display
epd = epd7in5bc.EPD()

def internet(host="8.8.8.8", port=53, timeout=3):
    # check if an internet connection can be established.
    # if not then return an exception
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as e:
        logging.info("No internet")
        return False


def getIpAddress():
    ip_address = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def format_numbers(num):
    # format large numbers to a human format
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def get_data(config):
    pass


def display_exception():
    # TODO clear the screen
    # TODO show an error text with an image
    pass


def center_image(img):
    #get the positional arguments to place the image at the center
    width, height = img.size
    width = epd.width / 2 - width/2
    height = epd.height / 2 - height / 2
    return int(width), int(height)


def make_fig(config):
    # TODO create the sparkline
    # TODO create the graph
    # TODO set the graphs size
    # TODO set the font size
    # TODO have a gallery mode
    # TODO have a 2 split mode
    # TODO have a 4 split mode
    # TODO display messages in a window
    pass


def get_config():
    with open("config.json") as file:
        config = json.load(file)

    return config


def show_boot_screen(config):
    # TODO make Codingry boot logo in Yellow and black
    # TODO show the screen only for a set duration
    epd.init()
    epd.Clear()
    ip_address = Image.open(os.path.join(picdir, "ip_address.png"))
    x, y = center_image(ip_address)
    image = Image.new('L', (epd.height, epd.width), 255)  # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    image.paste(ip_address, (y, x))
    draw = ImageDraw.Draw(image)
    epd.display(epd.getbuffer(image), epd.getbuffer(image)) #TODO change this wrong usage of the black and white and yellow image!!
    time.sleep(config["boot_time"])
    pass


def update_display():
    pass


# noinspection PyBroadException
def make_qr_code(address: str, size: int = 150):
    # make a qr code for the ip address of the rpi
    # if that is not possible then TODO return an Error code and display it later
    try:
        img = qrcode.make(address)
        img.resize(size, size)
        # TODO resize the image if the size is given
        img.save(os.path.join(picdir, "ip_address.png"))
    except Exception as e:
        logging.info(str(e))


def main():
    # get the config file
    config = get_config()
    # TODO generate the qr code for the ip
    make_qr_code(getIpAddress(), 50)
    # TODO show the boot screen
    show_boot_screen(config)
    # TODO periodically update everything
    pass


if __name__ == '__main__':
    main()
