# TODO: THIS ENTIRE CLASS NEEDS UPDATE!! Because it no longer uses "Sess" and should now use "NAO"
import json


class SignalHandler:
    """
    Class that catches qi signals and connects them to callback methods
    The SIGNAL METHODS have to be called for it to take effect
    """

    def __init__(self, web_socket, nao_wrapper):
        self.ws = web_socket
        self.nao = nao_wrapper

    # --- SIGNAL METHODS ---

    def behaviour_started(self):
        """Catches the behaviorStarted signal"""
        self.nao.get_behaviour_manager().behaviorStarted.connect(self._starting_update)

    def behaviour_stopped(self):
        """Catches the behaviorStopped signal"""
        self.nao.get_behaviour_manager().behaviorStopped.connect(self._stopping_update)

    def speaking_done(self):
        """Connects callback method to the synchroTTS signal (called when text to speech completed)"""
        # self.sess.ALTextToSpeech.synchroTTS.connect(self._text_done)

    # --- CALLBACK METHODS ---

    def _starting_update(self, name):
        """This is a callback method called when behaviorStarted signal is fired"""
        msg = {'type': "Update", 'description': "Behaviour %s has started." % name, 'action': "Behaviour Started"}
        self.ws.send(json.dumps(msg))
        print("--BHVR STARTED--: " + name)

    def _stopping_update(self, name):
        """This is a callback method called when behaviorStopped signal is fired"""
        msg = {'type': "Update", 'description': "Behaviour %s has stopped." % name, 'action': "Behaviour Stopped"}
        self.ws.send(json.dumps(msg))
        print("--BHVR STOPPED--" + name)

    def _text_done(self, val):
        """Callback method when nao stops speaking"""
        msg = "Done talking. Value is: " + str(val)
        self.ws.send(json.dumps(msg))

    def _test_ws(self):
        self.ws.send("Test Message Sent From Signal Handler")
