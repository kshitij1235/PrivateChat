#pakages 

# connection modules 
import socket

# achive random values 
import random

import time 
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
            t2 = threading.Thread(target=server_.pull, args=())
            t2.start()
            print("thread 2 deploy")
        except:
            print("unable to load send messaage module (thread)")

        try:
            t3 = threading.Thread(target=server_.update, args=())
            t3.start()
            print("thread 3 deploy")
        except:
            print("unable to load send all messaage module (thread)")

        print("-----------------all-threats-depolyed----------------------------------")


    def update():
        while True:
            config_button['text'] = str(len(connected))+' USERS IN ROOM : '
            time.sleep(5)


    def doSomething():
        try:
            if len(connected)==0:
                root.destroy()
            else:
                for i in connected:
                    try:
                        print("SENDING MESSAGE TO CLIENT ABOUT DISCONNET....")
                        i.send(bytes('SERVER WAS CLOSED BY THE HOST','utf-8'))
                        print("DRSTROYING THE WINDOW")
                        exit()
                    except:
                        exit()
                        pass
        except:
            root.destroy()



    def push_all_client():
        while True:
            for i in connected:
                try:
                    i.send(bytes(rec_messages,'utf-8'))
                except:
                    print("failed to pushh all")

#this pulls the message 
    def pull():

        global rec_messages

        while True:

            # this loop when message recived 
            try:
            #reciving  message of  numberous cleint 
                for i in connected:
                    try:
                        rec_messages=(i.recv(10232).decode())
                        if rec_messages=='A':
                            continue
                        try:
                            id_to_remove=int(rec_messages)
                            print("removing",id_to_remove," .......")
                            connected.pop(id_to_remove-1)
                            continue
                        except:
                            pass
                        
                        view_window.insert(END,rec_messages+'')
                    #this is to push the message to output windows for user experience    
                    except:
                        pass
            # this is when message dont recived 
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
        global connected #data of connected people (global ver toi make it accessableto everyone)
        global port 
        global username     #username of yours (this will be global)

        #vars 
        reconnect=0  #this var limits reconnecting attempt
        connected=[]  #ALL THE CONENCTED CONENTIONS 


        
        port=host_config.get()
        port=int(port[len_ip+1:len_ip+5])  #port number
        port_text=str(port) #port to display it to user

        username=username_config.get()  #GET USER NAME

        # update the user 
        config_button['text'] = 'TRYING TO CONNECT.....'

        try:

            config_button['text'] = 'IP SET : '+fetch_ip

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
                config_button['text'] = 'CONNECTED TO PORT : '+str(port)
                config_button.config(bg='light green')

            except:

                reconnect=reconnect+1

                #this is update to status menu in gui
                config_button['text'] = 'PROBLEM CONNECTING'+str(port)
                config_button.config(bg='red')

                if reconnect>4:
                    server_.port_cheak()

        except: 
            config_button['text'] = 'COULD NOT CONNECT'
            config_button.config(bg='red')

            if reconnect>4:
                server_.port_cheak()

        config_button['text'] = 'CONNECTED ON PORT : '+str(port)

        #all the connection work is handel here 

    
        print("waiting...")  #update the console 

    # accepting conenctions 


# signal for the client 

#GETTING THE USERNAME



        view_window.config(bg='white')

        while True:
            c,addr=server.accept()
            connected.append(c)
            print(socket.gethostname()," entered the room")
            c.send(bytes(str(len(connected)),'utf-8'))
            
            print(connected)
            c.send(bytes("WELCOME TO SERVER : "+username,'utf-8'))
            print("connected with ",addr)
            print(connected)
            
    



                   
#programs     

# gui code 
   
root = tk.Tk()

#TITLE
root.title("server")

try:
    root.iconbitmap('F:\kshitij\python\prichat\chat app\chat\media\icon_chat_app.ico')
except:
    print("cant load icon")

#color of background
root.config(bg="white")

#SCREENSIZE
root.geometry("300x391")
root.minsize(300,391)
root.maxsize(300,391)

 
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
fetch_hostname='SERVER'+str(random.randint(100,9999))


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
view_window= Text(root, width=38,height=17,bg='grey',borderwidth=0)
view_window.place(y=65,x=0)

# text message section   
message_ = tk.Entry(root,borderwidth=1)
message_.place(x =0,y = 340,width=245,height=47)

# message sending 
send_button = Button(root, text ="send",height=3,width=8,borderwidth=0,bg='light green',command=server_.push) 
send_button.place(x=244, y=340)
root.bind('<Return>',lambda event:server_.push())

root.protocol('WM_DELETE_WINDOW', server_.doSomething)  

root.mainloop()