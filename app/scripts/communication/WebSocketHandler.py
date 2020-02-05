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
        """This method is from Tornado for getting parameters passed into websocket handler"""
        self.nao = nao_wrapper  # do not do in __init__

    def data_received(self, chunk):
        """Not sure (yet) how/when to use this method, but needed to implement it so I did"""
        pass

    def open(self):
        print('New connection')
        data = {'type': "Info", 'action': "Client Connected", 'description': "You have successfully connected"}
        self.request_handler = RequestHandler(self.nao)
        self.signal_handler = SignalHandler(self, self.nao)  # init classes here, that want to send messages to client

        # connect signal handlers
        self.signal_handler.behaviour_started()
        self.signal_handler.behaviour_stopped()
        self.signal_handler.speaking_done()  # this is optional (for testing)

        self.write_message(json.dumps(data))    # send the "welcome message"

    def on_message(self, message):
        print 'Client said:  %s' % message
        # TODO - checks needed for this 'response'; lots of room for errors
        response = self.request_handler.get_response(message)

        print 'Sending Back: %s' % response
        self.write_message(response)

    def on_close(self):
        print('Connection closed.')

    def check_origin(self, origin):
        return True

    def send(self, message):
        """For use by outside classes who want WebSocket to write message to client
        Not sure if separating it like this provides any benefit  - but I like to think it does"""
        # TODO maybe modify this method to accept a type/action/description, then use request handler to make
        #  response before sending? (also maybe use a consistent term: either message or response?)
        self.write_message(message)
