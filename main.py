# general imports
import os.path
import socket
import logging
import qrcode
import math
import time

# imports
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
from waveshare_epd import epd7in5bc
import json
import locale
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
mpl.use("Agg")

# paths
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
plotdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
josefin_regular = ImageFont.truetype(os.path.join(fontdir, 'JosefinSans-Regular.ttf'), 30)
josefin_bold = ImageFont.truetype(os.path.join(fontdir, 'JosefinSans-Bold.ttf'), 30)

# display
epd = epd7in5bc.EPD()

# flags
loggedException = False


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


def plot_ticker(config):
    pass


def display_exception():
    # TODO clear the screen
    # TODO show an error text with an image
    pass


def center_image(img):
    # get the positional arguments to place the image at the center
    width, height = img.size
    width = epd.width / 2 - width / 2
    height = epd.height / 2 - height / 2
    return int(width), int(height)


def make_fig(ticker_name: str = 'MSFT'):
    # TODO switch from Plotly to Matplotlib due to shitty kaleido support

    # get the ticker
    ticker = yf.Ticker(ticker_name)
    hist = ticker.history(period='7d', interval='5m', prepost=True)

    # TODO create the graph

    # TODO resize the graph
    # TODO save the image as plot.png


def get_config():
    with open("config.json") as file:
        config = json.load(file)

    return config


def show_boot_screen(config):
    epd.init()
    epd.Clear()
    ip_address = Image.open(os.path.join(picdir, "plot.png"))
    x, y = center_image(ip_address)
    # 255: clear the image with white
    image = Image.new('L', (epd.height, epd.width), 255)
    # TODO make Codingry boot logo
    draw = ImageDraw.Draw(image)
    draw.text((15, 100), 'Scan the QR code to open the settings page', font=josefin_bold, fill=0)
    image.paste(ip_address, (y, x))
    epd.display(epd.getbuffer(image),
                epd.getbuffer(image))  # TODO change this wrong usage of the black and white and yellow image!!!
    time.sleep(config["boot_time"])
    pass


def update_display():
    epd.Clear()
    # draw the plot
    plot = Image.open(os.path.join(plotdir, "plot.png"))
    x, y = center_image(plot)
    image = Image.new('L', (epd.height, epd.width), 255)  # 255: clear the image with white
    image.paste(plot, (y, x))
    epd.display(epd.getbuffer(image), epd.getbuffer(image))
    pass


# noinspection PyBroadException
def make_qr_code(address: str, size: int):
    # make a qr code for the ip address of the rpi
    # if that is not possible then TODO return an Error code and display it later
    try:
        img = qrcode.make(address)
        img = img.resize((size, size))
        # TODO resize the image if the size is given
        img.save(os.path.join(picdir, "plot.png"))
    except Exception as e:
        logging.info(str(e))


def main():
    # get the config file
    config = get_config()
    # TODO generate the qr code for the ip
    make_qr_code(getIpAddress(), 150)
    # TODO show the boot screen
    show_boot_screen(config)
    # TODO periodically update everything
    while not loggedException:
        make_fig('MSFT')
        update_display()
        time.sleep(config["refresh_rate"])
    pass


if __name__ == '__main__':
    # start the main loop
    main()
