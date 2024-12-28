'''
This module defines the behaviour of a client in your Chat Application
'''
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util
'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''


class Client:
    '''
    This is the main Client Class. 
    '''
    def __init__(self, username, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Client socket created
        self.sock.settimeout(None)
        self.name = username
        self.name = username
        self.sock.connect((dest, port))
        self.connect = True

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''
        client_username = self.name #Setting the username to the default name in the constructor
        self.sock.send(client_username.encode("utf-8")) #Sending this username to the server
        
        while self.connect:
            user_input = input() #Taking user input
            
            if user_input == "list": #If user input is a list send "list" to the server
                self.sock.send("list".encode("utf-8"))
                
            elif "msg" in user_input: #If user input starts with a msg send the entire string entered by user to the server
                self.sock.send(user_input.encode("utf-8"))
            
            elif 'file' in user_input: #If user input starts with a file send the entire string entered by user to the server
                self.sock.send(user_input.encode("utf-8"))
                
            elif user_input == "help": #Creating a help to assist the user with correct input formats
                print("1) Enter your username")
                print("2) Type list if you want to view the available users")
                print("3) If you want to send a message, first enter the list of usernames to which you want to send the message. Next, enter the message!")
                print("4) If you want to send a file, first enter the list of usernames to which you want to send the file. Next type the filename and then include the actual file separated by a space. ")
                print("5) If you want to disconnect, please type quit")
                
            elif user_input == "quit": #If the user wants to quit
                self.sock.send("quit".encode("utf-8"))
                print("quitting\n")
                self.connect = False #Need to disconnect the socket
            
            else:
                print("incorrect userinput format\n") #If the user enters something else besides the above mentioned inputs then throw an error
        
        # raise NotImplementedError

    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''
        while self.connect:
            server_response = self.sock.recv(4096).decode("utf-8") #Receive a response from the server
                    
            if 'err_server_full' in server_response : #If server is full throw the error and disconnect the client
                print('disconnected: server full\n')
                self.connect = False
                return
                
            elif 'err_username_unavailable' in server_response : #If username is not available throw the error and disconnect the client
                print("disconnected: username not available\n")
                self.connect = False
                return
                
            elif "list" in server_response : #Server sends a sorted list of available users in ascending order
                received_list = server_response
                print(server_response)
                print("\n")
            
            elif "msg: client" in server_response : #Server sends back a message which is sent by another client intended for this client
                received_text = server_response
                print(received_text)
                print('\n')
            
            elif "file: client" in server_response : #Sending file to the correct user
                received_file = server_response 
                separated_list = received_file.split(',') 
                file_name = self.name+"_"+separated_list[1] #Setting name of the new file in which content needs to be stored
                file_content = separated_list[2] #This contains the file data that needs to be written to the new file
                client_output = "".join(separated_list[0]) #This contains the correct format which needs to be printed on client screen
                print(client_output)
                print('\n')
                with open(file_name,'wb') as file: #Writing file content in new file
                    file.write(file_content.encode())
                    
            elif "err_unknown_message" in server_response : #In case the client inputs a message that cant be recognised by the user
                print("disconnected: server received an unknown command\n")
            
            elif "quitting" in server_response : #Disconnect the client if it wants to quit
                self.connect = False
                return

        self.sock.close() #If the loop breaks close the socket



# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a", ["user=", "port=", "address="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()


