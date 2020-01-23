import json
import os.path

from .NaoQiWrapper import NaoQiWrapper


class RequestHandler:
    """
    Class to handle the messages Web Socket receives and treats them as requests
    This class assumes every message received on web socket is valid JSON; either a "request" or a "command"
    (kind of like my own versions of GET and PUT, but for the robot)
    """

    def __init__(self, nao_wrapper):
        self.response = "Default Response"
        self.nao = nao_wrapper

    def make_response(self, request):
        """Method used by web socket handler wanting to get a response to send client
        NOTE: Assuming request will be a valid JSON string"""

        data = {}  # create a dictionary which will be sent as JSON
        try:
            instruction = json.loads(request)
        except ValueError:
            self.response = "Error decoding request. Please send a valid JSON file."
            return self.response

        type = instruction['type']
        action = instruction['action']
        name = instruction['name']

        # TODO create JSON to send as response
        if type == "command":
            if action == "start":
                self.nao.start_behaviour(name)
                self.response = "Behaviour %s started" % name
            if action == "stop":
                self.nao.stop_behaviour(name)
                self.response = "Behaviour %s stopped" % name
        elif type == "request":  # NOTE: not using this for now; the app dev team wants to hard-code this!!
            # data['type'] = 'data'
            # data['message'] = 'This is the data you requested client'
            # data['array'] = ["quid", "pro", "quo"]
            abs_path = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(abs_path, "behaviours.json")
            with open(path) as f:
                data = json.load(f)
                json_string = json.dumps(data)
                # self.response = json_string
        else:
            self.response = "Unknown Request..."

        return self.response

