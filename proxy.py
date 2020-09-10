#!/usr/bin/env python3

from webthing import Thing, Property, Action, Value, SingleThing, WebThingServer
from tornado.ioloop import PeriodicCallback
from argparse import ArgumentParser
from requests import get
from uuid import uuid4


class ToggleAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid4().hex, thing, 'toggle', input_=input_)

    def perform_action(self):
        get('http://garage.home.internal/?action=toggle')
        self.thing.is_open.notify_of_external_update(
            value=not self.thing.is_open.get(),
        )


class GarageDoor(Thing):
    def __init__(self):
        super(GarageDoor, self).__init__(
            id_='urn:dev:ops:garage-door',
            title='Garage Door',
            type_=['DoorSensor'],
            description='The garage door',
        )
        self.is_open = Value(False)
        self.add_property(
            Property(
                thing=self,
                name='is_open',
                value=self.is_open,
                metadata={
                    '@type': 'OpenProperty',
                    'title': 'Open/Close',
                    'type': 'boolean',
                    'description': 'Whether the garage door is open',
                },
            ),
        )
        self.add_available_action(
            name='toggle',
            metadata={
                'title': 'Open/Close',
                '@type': 'ToggleAction',
                'description': 'Open/Close Garage Door',
            },
            cls=ToggleAction,
        )
        self.timer = PeriodicCallback(
            callback=self.update_level,
            callback_time=30000,
        )
        self.timer.start()

    def update_level(self):
        data = get('http://garage.home.internal/').json()
        if data.get('is_open') != self.is_open.get():
            self.is_open.notify_of_external_update(
                value=data.get('is_open'),
            )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--port',
        dest='port',
        type=int,
        default=8888,
    )
    args = parser.parse_args()
    garage_door = GarageDoor()
    server = WebThingServer(
        things=SingleThing(garage_door),
        port=args.port,
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
