from __future__ import print_function

import socket
import json
import threading
import os.path
import fnmatch  # for using unix-like wildcard

import qi

from .SignalHandler import SignalHandler


class Server:
    """
    This is the server that will run as background thread in Service.
    """

    def __init__(self, sess):
        """"""
        self.HOST = socket.gethostname()
        self.PORT = 9559  # Using port 9559, but could use any above 1024
        self.ADDR = socket.gethostbyname(socket.gethostname())  # ip address
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SESS = sess  # ref to qi session; allows accessing naoqi API modules (e.g. TextToSpeech)
        self.WRAPPER = self.SESS.WrapperService
        self.CLIENT_SOCK = None  # this is received when socket accepts a client

    def update_client(self, msg):
        """Method to be called by outside classes when they want to make server send something to client"""
        self._send_response(msg)

    def test(self):
        """Method for testing qi signals"""
        self.SESS.ALTextToSpeech.say("TESTING SERVER!")
        s = qi.Signal()  # create signal
        s.connect(self._on_signal)  # connect callback method
        s(42)  # trigger signal

        # self.SESS.ALTextToSpeech.say("My secret value is %s" % value)

    def serve(self):
        """Sets up a socket on port 9559 for listening to client connections"""
        self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # this is for reusing address
        self.SOCK.bind((self.ADDR, self.PORT))  # binds sock to ip and port
        print("Server created at: " + str(self.ADDR) + ", listening on port: " + str(self.PORT))
        self.SOCK.listen(0)
        # NOTE: I never close the socket (client should open and close connection)

        while True:
            print("Waiting for connection...")
            self.CLIENT_SOCK, client_address = self.SOCK.accept()  # accept connection
            self._send_response("You have connected!")
            print("Connection from: " + str(client_address[0]))  # first element in tuple is IP addr

            # starts a new background thread for handling requests
            thread = threading.Thread(target=self._handle_request)
            thread.setDaemon = True
            thread.run()

            # handle the signals when a behaviour starts or stops
            signal_handler = SignalHandler(self, self.SESS)
            signal_handler.behaviour_started()
            signal_handler.behaviour_stopped()
            signal_handler.speaking_done()  # this is optional (for testing)

    def _handle_request(self):
        """
        Handles request on server socket that client made
        """
        while True:
            request = self.CLIENT_SOCK.recv(2048)  # receive data from client

            if not request:
                print("Client disconnected")
                break

            # do some sort of string parsing here (either json or csv)
            # client just needs to start or stop mostly
            # client should also pass what exactly they want to start/stop
            # parse the strings to create the appropriate "run behaviour" string/path

            # Steps:
            # 1. get required "command" i.e. start, stop, stopall, what ever else you want to allow
            # 2. get the paramaters, and form the appropriate string (e.g. "elbow/elbow-flexion" for exercise)
            # 3. create appropriate formatted string to send as response back to client (e.g. behaviour started)

            print("Client said: " + request)
            message = self._parse_request(request)
            self._send_response("I got your request -> %s" % request)

            # TODO: Obviously get rid of all these 'if' statements. Refactor this later...
            if request:
                # sock.send("I received your request to -> " + request)
                if request == "stop":
                    self.SESS.ALBehaviorManager.stopAllBehaviors()
                if request == "dance":
                    self.SESS.ALBehaviorManager.startBehavior("dances/Macarena")
                if request == "running":
                    running = self.SESS.ALBehaviorManager.getRunningBehaviors()
                    print(*running, sep='\n')
                if request == "list":
                    all_list = self.SESS.ALBehaviorManager.getInstalledBehaviors()
                    print(*all_list, sep='\n')
                if request == "taichi":
                    self.SESS.ALBehaviorManager.startBehavior("taichi-dance-free")
                if request == "hip-flexion":
                    self.SESS.ALBehaviorManager.stopBehavior("fall-recovery/plugin")
                    self.SESS.ALBehaviorManager.startBehavior("hips/hip-flexion")
                if request == "knee-extension":
                    self.SESS.ALBehaviorManager.startBehavior("knees/knee-extension")
                if request == "knee-flexion":
                    self.SESS.ALBehaviorManager.startBehavior("ankles/knee-flexion")
                if request == "wrists":
                    self.SESS.ALBehaviorManager.startBehavior("wrists/FingersFlexed")
                if request == "shoulder-rotation":
                    self.SESS.ALBehaviorManager.startBehavior("shoulders/shoulder-rotation")
                if request == "test":
                    self.test()
                if request == "update":
                    self._send_response("Here is your update client...")
                if fnmatch.fnmatch(request, 'msg:*'):
                    self._send_response("I got the msg")
                if fnmatch.fnmatch(request, 'iam:*'):
                    self._send_response("iam:NAO")
                if request == "data":
                    abs_path = os.path.abspath(os.path.dirname(__file__))
                    path = os.path.join(abs_path, "behaviours.json")
                    with open(path) as f:
                        data = json.load(f)
                        json_string = json.dumps(data)
                        # sock.send(json_string) - dont send here!
                        print(json_string)

                # self._send_response(request)

    def _send_response(self, request):
        """Sends a response to the connected client"""
        self.CLIENT_SOCK.send(request)
        print("Server responded: " + request)

    def _on_signal(self, value):
        """Test callback method for qi signal"""
        # send the client the value (this method not working)
        msg = "The signal value is %s" % value
        # self.CLIENT_SOCK.sendall("The signal value is %s" % value)
        self._send_response(msg)

    def _parse_request(self, request):
        """Method for parsing a CSV message request"""
        arr = request.split(":")
        print("Parsing request...")
        for a in arr:
            print(a)

        # assume that first value is the command to execute
        if arr[0] == "cmd":
            self._send_response("~~~CMD.EXE~~~")
        print("...Finished parsing")
        return arr[0]
