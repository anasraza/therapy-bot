

# TODO: THIS ENTIRE CLASS NEEDS UPDATE!! Because it no longer uses "Sess" and should now use "NAO"
class SignalHandler:
    """Class that catches qi signals and connects them to callback methods"""

    def __init__(self, web_socket):
        self.ws = web_socket

    # --- SIGNALS ---

    def behaviour_started(self):
        """Catches the behaviorStarted signal"""
        # self.sess.ALBehaviorManager.behaviorStarted.connect(self._running_update)

    def behaviour_stopped(self):
        """Catches the behaviorStopped signal"""
        # self.sess.ALBehaviorManager.behaviorStopped.connect(self._stopping_update)

    def speaking_done(self):
        """Connects callback method to the synchroTTS signal (called when text to speech completed)"""
        # self.sess.ALTextToSpeech.synchroTTS.connect(self._text_done)

    # --- CALLBACK METHODS ---

    def _running_update(self, name):
        """This is a callback method called when behaviorStarted signal is fired"""
        msg = "Behaviour %s is running!" % name
        self.ws.send(msg)
        print("Callback: " + msg)

    def _stopping_update(self, name):
        """This is a callback method called when behaviorStopped signal is fired"""
        msg = "Behaviour %s has stopped!" % name
        self.ws.send(msg)
        print("Callback: " + msg)

    def _text_done(self, val):
        msg = "Done talking. Value is: " + str(val)
        self.ws.send(msg)
        print("Callback: " + msg)

    def _test_ws(self):
        self.ws.send("Test Message Sent From Signal Handler")
