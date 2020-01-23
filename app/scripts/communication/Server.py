from __future__ import print_function

import socket
import json
import threading
import os.path
import fnmatch  # for using unix-like wildcard

import qi

from .SignalHandler import SignalHandler
from .WebSocketHandler import WebSocketHandler
import tornado.web


class Server:
    """
    Sets up a Tornado WebSocketServer.
    """

    def __init__(self, nao_wrapper):
        self.PORT = 9999  # Could use any above 1024 (Maybe dont use port 9559)
        self.ADDR = socket.gethostbyname(socket.gethostname())  # ip address
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO change below to a Nao wrapper instead
        self.NAO = nao_wrapper
        self.WS = None

    # TODO: DELETE THIS LATER IF NOT NEEDED
    def test_signal(self):
        """Method for testing qi signals"""
        self.NAO.speak("TESTING SERVER!")
        s = qi.Signal()  # create signal
        s.connect(self._on_signal)  # connect callback method
        s(42)  # trigger signal

        # self.SESS.ALTextToSpeech.say("My secret value is %s" % value)

    # TODO: CHANGE DOC STRING LATER
    def serve(self):
        """
        Sets up a tornado web socket server on url '<ADDR>:<PORT>'
        ! WARNING: I have done no checks for GET calls on other URLs
        """

        # TODO: Include Websocket here somewhere...

        # setting up a tornado web socket server (using the websockethandler class)
        application = tornado.web.Application([(r'/', WebSocketHandler, dict(nao_wrapper=self.NAO))])
        application.listen(self.PORT)
        print('WebSocket server started at ADDRESS %s on PORT %s ' % (self.ADDR, self.PORT))
        tornado.ioloop.IOLoop.instance().start()
        # this is blocking - use background thread if want to continue after this point

        # ___IGNORE CODE BELOW FOR NOW___
        # handle the signals when a behaviour starts or stops
        signal_handler = SignalHandler(self)
        signal_handler.behaviour_started()
        signal_handler.behaviour_stopped()
        signal_handler.speaking_done()  # this is optional (for testing)

    def _on_signal(self, value):
        """Test callback method for qi signal"""
        # send the client the value (this method not working)
        msg = "The signal value is %s" % value
        # self.CLIENT_SOCK.sendall("The signal value is %s" % value)
