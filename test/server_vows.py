#!/usr/bin/python

from pyvows import Vows
from pyvows import expect


@Vows.batch
class WebsocketServer(Vows.Context):

    def setup(self):
        pass

    def teardown(self):
        pass

    def topic(self):
        return 'ok'

    def tests_are_working(self, topic):
        expect(topic).Not.to_be_null()
