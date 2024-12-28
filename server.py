'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util
import pickle
import threading
import base64

MAX_NUM_CLIENTS = 10
class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''
    def __init__(self, dest, port):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.client_usernames =[] #List to store client usernames
        self.client_dictionary ={} #Dictionary to store client socket and their corresponding usernames
    
    def handle_client(self, connectionSocket , client_address):
        client_username = connectionSocket.recv(4096).decode("utf-8") #Initially the client will send username once it gets connected
        
        def find_length(lst): #Using this later in msg and list
            count = 0
            for i in lst:
                count=count+1
            return count
        
        num_clients_connected = len(self.client_dictionary) + 1  #Number of users connected
        
        if num_clients_connected > 10: #If number of users connected is greater than 10, disconnect the socket
            connectionSocket.send('err_server_full'.encode("utf-8"))
            print("disconnected: server full\n")
            connectionSocket.close()
            
        elif client_username in self.client_usernames: #If a client tries to join by entering the same username display an error
            connectionSocket.send('err_username_unavailable'.encode("utf-8"))
            print("disconnected: username not available\n")
            connectionSocket.close()
            
        elif num_clients_connected <= 10: #If the number of users are less than or equal to 10, allow the user to join
            self.client_dictionary[connectionSocket] = client_username #Storing the client username corresponding to a socket
            self.client_usernames.append(client_username) #Add the username to the list of usernames
            print(f"join: {client_username}\n")
            
            while True:   
                client_request = connectionSocket.recv(4096).decode("utf-8")  #Receiving client requests
                
                if "list" in client_request:     
                    print(f"request_users_list: {client_username}") 
                    self.client_usernames.sort() #Sorting in ascending order the list of usernames
                    lst_of_users = " ".join(str(x) for x in self.client_usernames) #Joining the elements of the list by a space
                    lst = "list: " + lst_of_users #Sending list message in correct format
                    connectionSocket.send(lst.encode("utf-8"))
                    
                elif "msg" in client_request:
                    message_parts = client_request.split()
                    num_recipients = int(message_parts[1]) #First index will comprise of number of recipients
                    index = 2 + num_recipients
                    recipient_usernames = message_parts[2:index] #Recipient usernames will be mentioned from the 2 index to the index 2+number_recipients
                    receiver_usernames = list(set(recipient_usernames)) #Removing duplicate usernames
                    client_message = message_parts[index:] #Message to be sent will be in this index
                    message_send = " ".join(client_message) #Join the message by spaces
                    message_to_send = "msg: "+client_username+":"+" "+message_send #Display this msg on clients terminal
    
                    recipients = [] 
                    recipients_not_found = []
                    
                    for sock in self.client_dictionary: #Loop to add the recipients to whom message should be sent in a loop
                        if self.client_dictionary[sock] in receiver_usernames:
                            recipients.append(sock)
                    
                    for i in receiver_usernames: #Loop to check if wrong usernames have been entered
                        if i not in self.client_usernames:
                            recipients_not_found.append(i)
    
                    length_of_recipients = find_length(recipients)  
                    length_of_recipients_not_found = find_length(recipients_not_found)      
                    
                    #Message will only be sent if number of recipients is greater than 0 and will send message to the client sockets in recipients(to whom file should be sent)
                    print(f"msg: {client_username}\n")
                    for sock in recipients:
                        sock.send(message_to_send.encode()) 
                              
                    if length_of_recipients_not_found > 0: #For all such usernames who dont exist in the client directory
                        not_found = ' '.join(recipients_not_found)
                        print (f"msg: {client_username} to non-existent user {not_found}\n")
                        
                        
                elif "file" in client_request:  
                    message_parts = client_request.split()
                    num_recipients = int(message_parts[1])  #First index will comprise of number of recipients
                    index = 2 + num_recipients
                    recipient_usernames = message_parts[2:index] #Recipient usernames will be mentioned from the 2 index to the index 2+number_recipients
                    receiver_usernames = list(set(recipient_usernames)) #Removing duplicate usernames
                    file_naming = message_parts[index:index+1] #Filename will be present at that index
                    file_name = "".join(file_naming) #Saving it as a string so could be encoded
                    client_file = message_parts[index+1:] #File data
                    
                    with open(file_name,'rb') as file: #Reading the file
                        file_data = file.read()
                        
                    decoded_data = file_data.decode('utf-8') 
                    string = "file: " + client_username + ": " + file_name + "," + file_name + ","+decoded_data #Sending everything so that the filename and data can be separated on the basis of commas and client can easily save the filename and data
                    file_to_send = f'{string} {file_data}'
                    recipients = [] 
                    recipients_not_found = []
                    
                    for sock in self.client_dictionary: #Loop to add the recipients to whom message should be sent in a loop
                        if self.client_dictionary[sock] in receiver_usernames:
                            recipients.append(sock)
                            
                    for i in receiver_usernames:  #Loop to check if wrong usernames have been entered
                        if i not in self.client_usernames:
                            recipients_not_found.append(i)
                                         
                    length_of_recipients = find_length(recipients)  
                    length_of_recipients_not_found=find_length(recipients_not_found)    
                    
                    #file will only be sent if number of recipients is greater than 0 and will send file to the client sockets in recipients(to whom file should be sent)
                    print(f"file: {client_username}\n")
                    for sock in recipients:
                        sock.send(string.encode())
                              
                    if length_of_recipients_not_found > 0: #For all such usernames who dont exist in the client directory
                        not_found = ' '.join(recipients_not_found)
                        print(f"file: {client_username} to non-existent user {not_found}\n")
                           
                            
                elif "quit" in client_request: 
                    connectionSocket.send("quitting".encode("utf-8"))
                    del self.client_dictionary[connectionSocket] #If the user quits, delete its socket 
                    self.client_usernames.remove(client_username) #Remove its name from the list of usernames
                    connectionSocket.close() #Close the socket
                    print(f"disconnected: {client_username}\n")
                    break
                
                else:
                    connectionSocket.send('err_unknown_message'.encode("utf-8"))

                            
    def start(self):
        '''
        Main loop.
        continue receiving messages from Clients and processing it
        '''    
        self.sock.listen()
        while 1:
            connectionSocket, client_address= self.sock.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(connectionSocket, client_address))
            client_thread.start()          
        # raise NotImplementedError

# Do not change this part of code


if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a", ["port=", "address="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a

    SERVER = Server(DEST, PORT)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
