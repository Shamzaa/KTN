# -*- coding: utf-8 -*-
import socketserver
import json
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
clients = {};
history = [];

commands = "\nCommands:\n\tlogin <username>\n\tlogout\n\tmsg <message>\n\tnames\n\thelp";
welcomeMessage = """
 __      __       .__                               
/  \    /  \ ____ |  |   ____  ____   _____   ____  
\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ 
 \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ 
  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >
       \/       \/          \/            \/     \/ 

""";
class parser():
    def parse(self,received_string):
        received_json = json.loads(received_string);
        if(received_json["request"] in self.parse_tabel):
            return self.parse_tabel[received_json["request"]](self,received_json["content"]);
            
    parse_tabel = {};
    
    
class ClientHandler(socketserver.BaseRequestHandler,parser):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0];
        self.port = self.client_address[1];
        self.connection = self.request;
        
        self.username = None;
        self.isAdmin = False;
        
        print("New client connected!");
        
        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(4096).decode("UTF-8");
                self.parse(received_string);
            except Exception as e:
                print("Exception cought: {}\nTerminating connection!".format(e));
                
                break;
        # Clean up
        if(self.username in clients):
            clients.pop(self.username);
        self.connection.close();
        
        
    # variable data is dictionary
    def sendToUser(self,data):
        if not("timestamp" in data):
            data["timestamp"] = str(datetime.datetime.now().time().replace(microsecond = 0));
        
        m = ("{:0>4}".format(len(json.dumps(data))) + json.dumps(data)).encode("ASCII");
        print(m);
        self.connection.send(m);
        # data is dict
        # add server as sender
        # add timestamp
    
    @classmethod
    def sendToAllUsers(cls, data):
        data["timestamp"] = str(datetime.datetime.now().time().replace(microsecond = 0));
        history.append(data);
        for k,v in clients.items():
            v.sendToUser(data);
            
    def isLoggedIn(self):
        return self.username in clients;
        
    def login(self,username):
        if(self.isLoggedIn()):
            self.sendToUser(self.error("du er allerede logget inn"));
            
        if(not username in clients):
            clients[username] = self;
            self.username = username;
            self.sendToUser(ClientHandler.history());
            self.sendToUser(self.info(welcomeMessage));
            ClientHandler.sendToAllUsers(self.info("{}  har logget in".format(username)));
        else:
            self.sendToUser(self.error("brukernavnet er tatt"));
            
    def logout(self, message):

        if(self.isLoggedIn()):
            clients.pop(self.username);
            self.sendToUser(self.info("logget ut"));
        else:
            self.sendToUser(self.error("du er ikke logget inn, og kan ikke logge ut"));
    
    def msg(self,mess):
        # ja, det er et mess
        if(self.isLoggedIn()):
            ClientHandler.sendToAllUsers(self.message(mess));
        else:
            self.sendToUser(self.error("Du må logge in for å sende meldinger!"));
            
    def names(self,_):
        msg = "\n";
        for i in clients.keys():
            msg += "  " + i + "\n";
        self.sendToUser(self.info(msg));
    
    def help(self,_):
        self.sendToUser(self.info(commands));
    
    def message(self, message):
        return {
            "response": "message",
            "content": message,
            "sender": self.username
        };
    
    
    def error(self, message):
        return {
            "response": "error",
            "content": message,
            "sender": "Server"
        }
            
        
        
    def info(self, message):
        return {
            "response": "info",
            "content": message,
            "sender": "Server"
        };
    @classmethod
    def history(cls):
        return {
            "response": "history",
            "content": history,
            "sender": "Server"
        };
    
    
    #moderator
    
    def mod(self, message):
        if(self.isLoggedIn):
            self.isAdmin = message == "myNamaChef";
            if(self.isAdmin):
                self.sendToUser(self.info("du er nå admin"));
        
    def ban(self, message):
        # shitty if statement, yolo.
        if(message in clients and self.isAdmin and not(message == self.username)):
            ClientHandler.sendToAllUsers(self.info("{} has been banned".format(message)));
            clients.pop(message);

        
    parse_tabel = {
        "login": login,
        "logout": logout,
        "help": help,
        "msg": msg,
        "names": names,
        "mod": mod,
        "ban": ban
    }
    

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = ('0.0.0.0', 9998);
    print("Server running...2");

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler);
    server.serve_forever();
