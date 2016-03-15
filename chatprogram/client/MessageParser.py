import json

#'static' class
class MessageParser():
    
    def parse(cls, payload):
        payload = json.loads(payload);
        if payload['response'] in self.responseTable:
            return self.responseTable[payload['response']](payload);
        else:
            #Error?
            pass;

    def parse_error(cls, payload):
        pass;
    def parse_info(cls, payload):
        parse 
        pass;
    def parse_message(cls, payload):
        return "[{}] {}: {}".format(payload["timestamp"],payload["sender"],payload["content"]);
        pass;
    def parse_history(cls, payload):
        ret = "";
        for i,v in enumerate(payload["content"]):
            ret += cls.parse(v) + "\n";
        ret += "-" * 15;
        return ret;
    #Static:
    responseTable = {
        "error": parse_error,
        "info": parse_info,
        "history": parse_history,
        "message": parse_message
    }
    