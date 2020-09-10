from machine import Pin
from time import sleep


class Garage(object):
    SENSOR = Pin(12, Pin.IN, Pin.PULL_UP)
    RELAY = Pin(14, Pin.OUT)

    def is_open(self):
        return bool(self.SENSOR.value())

    def get(self, data):
        action = getattr(self, data.get('action', ''), None)
        if action:
            action()
        return dict(
            is_open=self.is_open(),
        )

    def toggle(self):
        self.RELAY.value(1)
        sleep(0.1)
        self.RELAY.value(0)
