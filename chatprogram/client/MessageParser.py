import json

#'static' class
class MessageParser():
    
    @classmethod
    def parse(cls, payload):
        if payload['response'] in cls.responseTable:
            return cls.responseTable[payload['response']](payload);
        else:
            #Error?
            pass;
    @classmethod
    def parse_error(cls, payload):
        return cls.parse_message(payload);
        pass;
    @classmethod
    def parse_info(cls, payload):
        return cls.parse_message(payload);
        pass;
    @classmethod
    def parse_message(cls, payload):
        return "[{}] {}: {}".format(payload["timestamp"],payload["sender"],payload["content"]);
        pass;
    @classmethod
    def parse_history(cls, payload):
        ret = "";
        for i,v in enumerate(payload["content"]):
            ret += cls.parse(v) + "\n";
        ret += "-" * 15;
        return ret;
    
    
MessageParser.responseTable = {
    "error": MessageParser.parse_error,
    "info": MessageParser.parse_info,
    "history": MessageParser.parse_history,
    "message": MessageParser.parse_message
}