#pakages 

# connection modules 
import socket

# achive random values 
import random

# gui module 
import tkinter as tk
from tkinter import *

# module to improve modules 
import threading
import tkinter
from typing import Generator


# class 

class server_():

    # fuctions 

    #this fuction unlocks threading to run things multiple

    def unlock():
        print("-----------------deploying-threats----------------------------------")
        try:
            t1 = threading.Thread(target=server_.port_cheak, args=())
            t1.start()
            print("threat 1 deploy")
        except:
            print("unable to start ;( ")

        try:
            t2 = threading.Thread(target=server_.push, args=())
            t2.start()
            print("thread 2 deploy")
        except:
            print("unable to load send messaage module (thread)")


        t3 = threading.Thread(target=server_.pull, args=())
        t3.start()
        print("-----------------all-threats-depolyed----------------------------------")


    def pull():
        while True:
            try:
                for i in connected:
                    try:
                        rec_messages=(i.recv(10232).decode())
                        try:
                            id_to_remove=int(rec_messages)
                            print("removing",id_to_remove," .......")
                            connected.pop(id_to_remove-1)

                        except:
                            pass
                        template=rec_messages+'\n'
                        view_window.insert(END,template)
                    except:
                        pass

            except:
                continue


# this functions help to send message

    def push():
        print(connected)
        message=message_.get() # to get the value from teh message box 

        # this helps to keep  to avoid empty messages 

        if message=='':
            pass
        
        else:
            
            # to detect the typed messsage 
            print("message typed : ",message)
            
            # refresh the chat box
            message_.delete(0,"end")

            # to send message in particular fassion 
            send_template=username +' : '+message+'\n'
            for i in connected:
                # to send the message 
                i.send(bytes(send_template,'utf-8'))

            # this template is for your frame of refrence 
            template='YOU : '+message+'\n'

            # update the view port of the user 
            view_window.insert(END,template) 
        

            return message


# this fuction connect you with your port 

    def port_cheak():

        #vars 
        reconnect=0  #this var limits reconnecting attempt

        ip=fetch_ip

        global connected #data of connected people (global ver toi make it accessableto everyone)
        connected=[]
        
        global port 
        port=host_config.get()
        port=int(port[len_ip+1:len_ip+5])  #port number
        port_text=str(port) #port to display it to user

        global username     #username of yours (this will be global)
        username=username_config.get()


        # update the user 
        config_button['text'] = 'TRYING TO CONNECT.....'

        try:

            config_button['text'] = 'IP SET : '+ip

            try: 

                # creating socket 
                try:
                    server=socket.socket()
                    print("socket created")
                except socket.error as msg:
                    server=None
                    server_.port_cheak()

                # generating a random port number so that it wont show any occupied the next time using the same one 
                print(fetch_ip)
                # binding the socket
                server.bind((fetch_ip,port)) 

                #listing to particular amount of peoples request
                server.listen(3)


                # this is a update to status menu in gui 
                config_button['text'] = 'CONNECTED TO PORT : '+port_text
                config_button.config(bg='light green')

            except:

                reconnect=reconnect+1

                #this is update to status menu in gui
                config_button['text'] = 'PROBLEM CONNECTING'+port_text
                config_button.config(bg='red')

                if reconnect>4:
                    server_.port_cheak()

        except: 
            config_button['text'] = 'COULD NOT CONNECT'
            config_button.config(bg='red')

            if reconnect>4:
                server_.port_cheak()

        config_button['text'] = 'WAITING ON PORT : '+port_text

        #all the connection work is handel here 

    
        print("waiting...")  #update the console 

    # accepting conenctions 


# signal for the client 

#GETTING THE USERNAME


        while True:
            view_window.config(bg='white')
            c,addr=server.accept()
            connected.append(c)
            c.send(bytes(str(len(connected)),'utf-8'))
            print(connected)
            c.send(bytes("you are connected to the server",'utf-8'))
            print("connected with ",addr)
            print(connected)
            
    



                   
#programs     

# gui code 
   
root = tk.Tk()

#TITLE
root.title("server")

try:
    root.iconbitmap('media//icon_chat_app.ico')
except:
    print("cant load icon")

#color of background
root.config(bg="white")

#SCREENSIZE
root.geometry("300x400")
root.minsize(300,400)
root.maxsize(300,400)

 
# status bar 

config_button = Button(root, text ="PRESS TO CONNECT",width=45,height=1, command=server_.unlock,borderwidth=0) 
config_button.place(x=0, y=0)

# details section 

# getting the users ip and hostname
fetch_hostname = socket.gethostname()

print("----------------basic--info-----------------------")

print("fetch hostname : ",fetch_hostname)
fetch_ip=socket.gethostbyname(fetch_hostname)

len_ip=len(fetch_ip)
print("ip_lenght : ",len_ip)

# Generator of username 
fetch_hostname='username'+str(random.randint(100,9999))


# PRINTING DETAILS 
print("generated username : ",fetch_hostname)
print("fetch_ip : ",fetch_ip)

print("------------------------------------------")

# HOST_IP ENTRY 
host_config = Entry(root)
host_config.place(x =0,y =25,width=150,height=35)
host_config.insert(END,fetch_ip+':9999')

# username ENTRY 
username_config = Entry(root)
username_config.place(x =150,y =25,width=151,height=35)
username_config.insert(END,fetch_hostname)

#message window
view_window= Text(root, width=38,height=19,bg='grey',borderwidth=0)
view_window.place(y=65,x=0)

# text message section   
message_ = tk.Entry(root,borderwidth=1)
message_.place(x =0,y = 345,width=245,height=47)

# message sending 
send_button = Button(root, text ="send",height=3,width=8,borderwidth=0,bg='light green',command=server_.push) 
send_button.place(x=244, y=346)
root.bind('<Return>',lambda event:server_.push())


root.mainloop()