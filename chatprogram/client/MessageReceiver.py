# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self);
        # Flag to run thread as a deamon
        self.daemon = True
        self.client = client;
        self.connection = connection;
        
    def run(self):
        #Listne for connections
        while True:
            res = self.connection.recv(4096);
            self.client.receive_message(res.decode("UTF-8"));
        