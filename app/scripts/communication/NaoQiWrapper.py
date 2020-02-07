class NaoQiWrapper:
    """
    Wrapper class that wraps the required NAOqi API modules
    It uses qi.Service instead of ALProxy, from the stk/services file (from the template by Emile Kroeger)
    """
    def __init__(self, qi_session):
        self.sess = qi_session    # qi_session (actually service cache from stk/services)
        self.tts = self.sess.ALTextToSpeech
        self.bm = self.sess.ALBehaviorManager
        self.al = self.sess.ALAutonomousLife
        self.rp = self.sess.ALRobotPosture
        # init whatever other API modules needed

    # Note: NAOqi API uses American-English spelling (e.g. no 'u' in 'behaviour'); I use British-English spelling
    def start_behaviour(self, name):
        """Assumes that 'name' is in correct format i.e. 'application-name/behaviour-name' as in Choregraphe'"""
        if not self.bm.isBehaviorInstalled(name):
            print("Error: Behaviour %s not installed." % name)
            return False
        if self.bm.isBehaviorRunning(name):
            print("Error: Behaviour %s is already running!" % name)
            return False
        # self.bm.startBehavior(name)
        self.al.switchFocus(name)
        return True

    def stop_behaviour(self, name):
        """Stops the behaviour if it is running and returns True"""
        if not self.bm.isBehaviorInstalled(name):
            print("Error: Behaviour %s not installed." % name)
            return False
        if not self.bm.isBehaviorRunning(name):
            print("Error: Behaviour %s is not running." % name)
            return False
        self.bm.stopBehavior(name)
        return True

    def stop_all_behaviours(self):
        """Stops all behaviours..."""
        self.bm.stopAllBehaviors()

    def speak(self, text):
        self.tts.say(text)

    # TODO change this to use the regular start-stop behaviour thing
    def go_to(self, position):
        """Goes to the position requested in command (last-minute addition) """
        if position == "sit":
            # self.rp.goToPosture("Sitting", 0.5) # doing 0.5 because that's what the behaviours used as well
            self.start_behaviour('dialog_posture/bhv_sit_down')
            return True
        if position == "stand":
            # self.rp.goToPosture("Stand", 0.5)
            self.start_behaviour('dialog_posture/bhv_stand_up')
            return True
        if position == "lie":
            # self.rp.goToPosture("LyingBack", 0.5)
            self.start_behaviour('dialog_posture/bhv_lie_down_back')    # this causes ERROR (fall-recovery kicks in)
            return True
        else:
            return False

    # ------------
    # API MODULES FOR CLASSES THAT MAY WANT THEM, as of now, signal handlers
    # This is an unusual design, but since right now only 2 modules are needed, it works. Refactor later.
    # -----------
    def get_behaviour_manager(self):
        return self.bm

    def get_text_to_speech(self):
        return self.tts



