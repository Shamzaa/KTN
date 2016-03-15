# -*- coding: utf-8 -*-
import socket
import re
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.host = host;
        self.server_port = server_port;
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.server_port))
    
    def run(self):
        while True:
            inp = input(">> ");
            match = re.search("^\\s*([^\\s]+)(?:$|\\s(.+))", inp);
            if(match):
                req = match.group(1);
                cont = match.group(2);
                
                request = {
                    "request": req,
                    "content": cont
                };
                self.send_payload(json.dumps(request).encode("ASCII"));
            else:
                pass;
                
                
    
    def receive_message(self, message):
        print(MessageParser.parse(message));
        
    def send_payload(self, data):
        self.connection.send(data);
        
    
if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client(input(), 9998);
    reqHandler = MessageReceiver(client,client.connection);
    reqHandler.start();
    client.run();    
