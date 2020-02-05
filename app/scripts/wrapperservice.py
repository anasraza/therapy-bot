"""
This template sets up a NAOqi service as a Python app.
In the manifest file, confirm that "autorun=true" so that this service starts at NAO startup
"""

import qi

import stk.runner
import stk.events
import stk.services
import stk.logging
import time

import threading

from communication.Server import Server
from communication.NaoQiWrapper import NaoQiWrapper


# TODO: use linter to make code conform to PEP-8
class WrapperService(object):
    """
    NAOqi service that is really only used to set up the server.
    Slightly hacky, but does the job (for now).
    It calls the setup() method, which runs a background thread with server. THAT'S IT
    Probably (most likely) not the best approach...but it works
    """

    # TODO: change this later
    APP_ID = "com.aldebaran.WrapperService"

    def __init__(self, qiapp):
        # generic activity boilerplate
        self.qiapp = qiapp
        self.events = stk.events.EventHelper(qiapp.session)
        self.s = stk.services.ServiceCache(qiapp.session)  # allows accessing API modules
        self.logger = stk.logging.get_logger(qiapp.session, self.APP_ID)
        # call the setup method to start server
        self.nao = NaoQiWrapper(self.s)  # wrapper for accessing nao api modules/methods
        self.setup()

        # Internal variables
        self.level = 0

    @qi.bind(returnType=qi.Void, paramsType=[])
    def setup(self):
        """Starts a server in background thread"""
        # time.sleep(60)
        # Starting the server as background thread
        self.nao.speak("Setting up server...")
        # create the server as background thread
        # pass the Nao Wrapper to server
        # NOTE: this thread is never closed
        thread = threading.Thread(target=Server(self.nao).serve)
        thread.daemon = True
        thread.start()

        # Server(self.s).test()

        self.nao.speak("Server is ready!")

    @qi.bind(returnType=qi.Void, paramsType=[qi.Int8])
    def set(self, level):
        """Set level"""
        self.level = level

    @qi.bind(returnType=qi.Int8, paramsType=[])
    def get(self):
        """Get level"""
        return self.level

    @qi.bind(returnType=qi.Void, paramsType=[])
    def reset(self):
        """Reset level to default value"""
        return self.set(0)

    @qi.bind(returnType=qi.Void, paramsType=[])
    def stop(self):
        """Stop the service."""
        self.logger.info("WrapperService stopped by user request.")
        self.qiapp.stop()

    @qi.nobind
    def on_stop(self):
        """Cleanup (add yours if needed)"""
        self.logger.info("WrapperService finished.")


####################
# Setup and Run
####################

if __name__ == "__main__":
    stk.runner.run_service(WrapperService)
