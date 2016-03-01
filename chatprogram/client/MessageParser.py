import json

class MessageParser():
    #Static:
    possible_responses = {
        "error": MessageParser.parse_error,
        "info": MessageParser.parse_info,
    # More key:values pairs are needed	
    }


    def __init__(self):
        pass;
        

    def parse(self, payload):
        payload = json.loads(payload);
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload);
        else:
            pass;

    def parse_error(self, payload):
        pass;
    def parse_info(self, payload):
        pass;
    # Include more methods for handling the different responses... 
