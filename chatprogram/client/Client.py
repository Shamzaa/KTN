# -*- coding: utf-8 -*-
import socket
import re
import json
import tkinter
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
        self.connection.connect((self.host, self.server_port));
        
    def send_message(self,inp):
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
    def inp_callback(self,a):
        self.send_message(self.e.get());
        self.e.delete(0, last=len(self.e.get()));
        
        
    def run(self):
        self.gui = tkinter.Tk();
        self.gui.geometry("450x450");
        self.t = tkinter.Text(self.gui,state='disabled');
        self.t.pack(expand=True, fill=tkinter.BOTH);
        self.e = tkinter.Entry(self.gui);
        self.e.bind("<Return>",self.inp_callback);
        self.e.pack(expand=True, fill=tkinter.X);
        self.gui.mainloop();
        
    
        while True:
            inp = input(">> ");
            self.send_message(inp);    
                
    
    def receive_message(self, message):
        self.t.configure(state="normal");
        self.t.insert('end', MessageParser.parse(json.loads(message)) + "\n");
        self.t.configure(state="disabled");
        #print(MessageParser.parse(json.loads(message)));
        
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
