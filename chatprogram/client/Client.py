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
        self.parser = MessageParser();
        self.connection.connect((self.host, self.server_port))
        # TODO: Finish init process with necessary code
    
    def run(self):
        # Initiate the connection to the server
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
                
                
    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print(self.parser.parse(message));
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(data);
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998);
    reqHandler = MessageReceiver(client,client.connection);
    print("Starting thread");
    reqHandler.start();
    print("Connecting to server!");
    client.run();    
