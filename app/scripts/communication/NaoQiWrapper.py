class NaoQiWrapper:
    """
    Wrapper class that wraps the required NAOqi API modules
    It uses qi.Service instead of ALProxy, from the stk/services file (from the template by Emile Kroeger)
    """
    def __init__(self, qi_session):
        self.sess = qi_session    # qi_session (actually service cache from stk/services)
        self.tts = self.sess.ALTextToSpeech
        self.bm = self.sess.ALBehaviorManager
        # init whatever other API modules needed

    # Note: NAOqi API uses American-English spelling (e.g. no 'u' in 'behaviour'); I use British-English spelling
    def start_behaviour(self, name):
        # TODO checks to make sure it is installed and not running already
        # self.bm.startBehavior(name)
        self.speak("Started Behaviour %s" % name)   # TODO remove these test speaks in these two methods

    def stop_behaviour(self, name):
        # self.bm.stopBehavior(name)
        self.speak("Stoped Behaviour %s" % name)

    def stop_all_behaviours(self):
        self.bm.stopAllBehaviors()

    def speak(self, text):
        self.tts.say(text)



