import json
import os.path

from .NaoQiWrapper import NaoQiWrapper


class RequestHandler:
    """
    Class to handle the messages Web Socket receives and treats them as requests
    This class assumes every message received on web socket is valid JSON; either a "request" or a "command"
    (kind of like my own versions of GET and PUT, but for the robot)
    NOTE: Tornado WebSocketHandler does have an overridable RequestHandler method that I am NOT using
    """

    def __init__(self, nao_wrapper):
        self.response = None  # will be set by the _make_response method
        self.nao = nao_wrapper
        self.type = None
        self.action = None
        self.description = None

    # TODO - this method does too much; should be split up
    def get_response(self, request):
        """Method used by web socket handler wanting to get a response to send client
        NOTE: Assuming request will be a valid JSON string"""

        try:
            instruction = json.loads(request)
        except ValueError:
            self.response = "Error decoding request. Please send a valid JSON file."
            return self.response

        # instruction = instruction.replace("")
        # TODO should have checks here for if the keys do not exist (right now I assume client follows format)
        self.type = instruction['type']
        self.action = instruction['action']
        self.description = instruction['description']

        # TODO probably could find a more elegant way of doing all this...
        if self.type == "command":
            if self.action == "start":
                # if behaviour names are hard-coded by client app, no need to use make_name()
                # in that case, the description is the name to be used (to call behaviour)
                if not self.nao.start_behaviour(self.description):
                    self._make_response('Error', 'Could Not Start Behaviour', 'Behaviour %s is not installed.'
                                        % self.description)
                    return self.response
                # IMPORTANT: This make_response below is *crucial* - otherwise WebSocket closes after each request
                # I have not reviewed the code well enough to understand why, but just do it for now...
                self._make_response('Update', 'Instruction Completed', 'Starting the requested behaviour...')
            elif self.action == "stop":
                if self.description == "all":
                    self.nao.stop_all_behaviours()
                    self._make_response('Update', 'Instruction Completed', 'Stopped all running behaviours!')
                if not self.nao.stop_behaviour(self.description):
                    self._make_response('Error', 'Could Not Stop Behaviour', 'Behaviour %s is not running.'
                                        % self.description)
                    return self.response

                # else do nothing (signal handler should automatically send response when behaviour starts/stops)
            elif self.action == "goto":
                if self.nao.go_to(self.description):
                    self._make_response('Update', 'Instruction Completed', 'Going to position %s.' % self.description)
                else:
                    self._make_response('Error', 'Invalid GoTo', 'Position %s is not valid' % self.description)
            else:
                # action not supported
                self._make_response('Error', 'Invalid Action', 'Action "%s" is not valid. See documentation for help.'
                                    % self.action)
                return self.response

        # elif type == "request":  # NOTE: not using this for now; the app dev team wants to hard-code this!!
        #     abs_path = os.path.abspath(os.path.dirname(__file__))   # get current directory
        #     path = os.path.join(abs_path, "behaviours.json")
        #     with open(path) as f:
        #         data = json.load(f)
        #         json_string = json.dumps(data)
        #         self.response = json_string
        else:
            self._make_response('Error', 'Invalid Type',
                                'Type "%s" is not valid. See documentation for help.' % self.type)
            return self.response

        # nothing went wrong, (the response should've been made/sent already)
        # self._make_response('Update', 'Instruction Completed', 'Instruction from client successfully completed!')
        return self.response

    def _make_response(self, type_, action, description):
        """
        Helper method for making the JSON response to be sent back to WebSocketHandler
        Params are the three dictionary keys/values
        Returns a string
        """
        response = {'type': type_, 'action': action, 'description': description}  # create a dictionary
        response_string = json.dumps(response)
        self.response = response_string

    def _make_name(self, string):
        """
        Helper method that takes a colon-seperated string and returns a name I can plug into Behaviour Manager
        e.g. if string is "hip:ely-test", name is "hip/ely-test"
        No need to use this if client app is hard-coding the names (just provide client behaviours.txt)
        Warning: the more you look at this, the stupider this looks.
        """
        arr = string.split(":")
        name = arr[1]
        return name
