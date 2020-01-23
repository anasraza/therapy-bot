import tornado.websocket
import tornado.web
import json

from .RequestHandler import RequestHandler
from .SignalHandler import SignalHandler


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """This is the handler for Tornado Websocket
    ! WARNING: Currently, multiple clients can connect!
    This is the whole point of websockets, but not what we need for this project!"""

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.request_handler = None
        self.signal_handler = None

    def initialize(self, nao_wrapper):
        self.nao = nao_wrapper

    def data_received(self, chunk):
        """Not sure (yet) how/when to use this method, but needed to implement it so I did"""
        pass

    def open(self):
        print('New connection')
        # self.write_message("Hello Client, you have connected")
        data = {'type': "Info", 'action': "Client Connected", 'name': "You have successfully connected"}
        self.request_handler = RequestHandler(self.nao)
        self.signal_handler = SignalHandler(self)  # init outside classes in open(), that want to use send(message)
        self.write_message(json.dumps(data))

    def on_message(self, message):
        print 'Client said:  %s' % message
        # TODO: parse this message as 'request'; client expected to follow format of msg;

        response = self.request_handler.make_response(message)

        print 'Sending Back: %s' % response
        self.write_message(response)
        # tts.say(message)

    def on_close(self):
        print('Connection closed.')

    def check_origin(self, origin):
        return True

    def send(self, message):
        """For use by outside classes who want WebSocket to write message to client
        Not sure if separating it like this provides any benefit  - but I like to think it does"""
        self.write_message(message)
