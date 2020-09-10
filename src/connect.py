from network import WLAN, STA_IF
from logging import LOGGER
from time import sleep


# TODO: read values from environmental variables?
SSID = 'SSID'
PASSWORD = 'PASSWORD'


def connect_to_ap():
    station = WLAN(STA_IF)
    if not station.active():
        station.active(True)
        if not station.isconnected():
            LOGGER.debug('Connecting....')
            station.connect(SSID, PASSWORD)
            while not station.isconnected():
                sleep(1)
    LOGGER.debug('Connected {}'.format(station.ifconfig()))
