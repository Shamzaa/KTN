import json

class MessageParser():
    
    def __init__(self):
        pass;
        
    def parse(self, payload):
        payload = json.loads(payload);
        if payload['response'] in self.responseTable:
            return self.responseTable[payload['response']](payload);
        else:
            #Error
            pass;

    def parse_error(self, payload):
        pass;
    def parse_info(self, payload):
        pass;
    def parse_message(self, payload):
        pass;
    def parse_history(self, payload):
        for i in payload["content"]:
            self.parse(i);
    #Static:
    responseTable = {
        "error": parse_error,
        "info": parse_info,
        "history": parse_history,
        "message": parse_message
        
    # More key:values pairs are needed	
    }
    
    # Include more methods for handling the different responses... 
